import torch
import torch.nn as nn
import torch.optim as optim
from MetaAugment.main import train_child_network, create_toy
from MetaAugment.autoaugment_learners.autoaugment import AutoAugment

import torchvision.transforms as transforms

import copy
import types




class aa_learner:
    """
    The parent class for all aa_learner's
    
    Attributes:
        op_tensor_length (int): what is the dimension of the tensor that represents
                            each 'operation' (which is made up of fun_name, prob,
                            and mag).
    """
    def __init__(self, 
                # parameters that define the search space
                sp_num=5,
                p_bins=11,
                m_bins=10,
                discrete_p_m=False,
                # hyperparameters for when training the child_network
                batch_size=32,
                toy_size=1,
                learning_rate=1e-1,
                max_epochs=float('inf'),
                early_stop_num=20,
                exclude_method = [],
                ):
        """
        Args:
            sp_num (int, optional): number of subpolicies per policy. Defaults to 5.
            fun_num (int, optional): number of image functions in our search space.
                            Defaults to 14.
            p_bins (int, optional): number of bins we divide the interval [0,1] for 
                            probabilities. Defaults to 11.
            m_bins (int, optional): number of bins we divide the magnitude space.
                            Defaults to 10.
            discrete_p_m (bool, optional):
                            Whether or not the agent should represent probability and 
                            magnitude as discrete variables as the out put of the 
                            controller (A controller can be a neural network, genetic
                            algorithm, etc.). Defaults to False
            
            batch_size (int, optional): child_network training parameter. Defaults to 32.
            toy_size (int, optional): child_network training parameter. ratio of original
                                dataset used in toy dataset. Defaults to 0.1.
            learning_rate (float, optional): child_network training parameter. Defaults to 1e-2.
            max_epochs (Union[int, float], optional): child_network training parameter. 
                                Defaults to float('inf').
            early_stop_num (int, optional): child_network training parameter. Defaults to 20.
        """
        # related to defining the search space
        self.sp_num = sp_num
        self.p_bins = p_bins
        self.m_bins = m_bins
        self.discrete_p_m = discrete_p_m

        # related to training of the child_network
        self.batch_size = batch_size
        self.toy_size = toy_size
        self.learning_rate = learning_rate

        self.max_epochs = max_epochs
        self.early_stop_num = early_stop_num

        # TODO: We should probably use a different way to store results than self.history
        self.history = []

        # this is the full augmentation space. We take out some image functions
        # if the user specifies so in the exclude_method parameter
        augmentation_space = [
            # (function_name, do_we_need_to_specify_magnitude)
            ("ShearX", True),
            ("ShearY", True),
            ("TranslateX", True),
            ("TranslateY", True),
            ("Rotate", True),
            ("Brightness", True),
            ("Color", True),
            ("Contrast", True),
            ("Sharpness", True),
            ("Posterize", True),
            ("Solarize", True),
            ("AutoContrast", False),
            ("Equalize", False),
            ("Invert", False),
        ]
        self.exclude_method = exclude_method
        self.augmentation_space = [x for x in augmentation_space if x[0] not in exclude_method]

        self.fun_num = len(self.augmentation_space)
        self.op_tensor_length = self.fun_num + p_bins + m_bins if discrete_p_m else self.fun_num +2


    def translate_operation_tensor(self, operation_tensor, return_log_prob=False, argmax=False):
        """
        takes in a tensor representing an operation and returns an actual operation which
        is in the form of:
            ("Invert", 0.8, None)
            or
            ("Contrast", 0.2, 6)

        Args:
            operation_tensor (tensor): 
                                We expect this tensor to already have been softmaxed.
                                Furthermore,
                                - If self.discrete_p_m is True, we expect to take in a tensor with
                                dimension (self.fun_num + self.p_bins + self.m_bins)
                                - If self.discrete_p_m is False, we expect to take in a tensor with
                                dimension (self.fun_num + 1 + 1)

            return_log_prob (boolesn): 
                                When this is on, we return which indices (of fun, prob, mag) were
                                chosen (either randomly or deterministically, depending on argmax).
                                This is used, for example, in the gru_learner to calculate the
                                probability of the actions were chosen, which is then logged, then
                                differentiated.

            argmax (boolean): 
                            Whether we are taking the argmax of the softmaxed tensors. 
                            If this is False, we treat the softmaxed outputs as multinomial pdf's.

        Returns:
            operation (list of tuples):
                                An operation in the format that can be directly put into an
                                AutoAugment object.
            log_prob (float):
                            Used in reinforcement learning updates, such as proximal policy update
                            in the gru_learner.
                            Can only be used when self.discrete_p_m.
                            We add the logged values of the indices of the image_function,
                            probability, and magnitude chosen.
                            This corresponds to multiplying the non-logged values, then logging
                            it.                  
        """

        if (not self.discrete_p_m) and return_log_prob:
            raise ValueError("You are not supposed to use return_log_prob=True when the agent's \
                            self.discrete_p_m is False!")

        # make sure shape is correct
        assert operation_tensor.shape==(self.op_tensor_length, ), operation_tensor.shape

        # if probability and magnitude are represented as discrete variables
        if self.discrete_p_m:
            fun_t, prob_t, mag_t = operation_tensor.split([self.fun_num, self.p_bins, self.m_bins])

            # make sure they are of right size
            assert fun_t.shape==(self.fun_num,), f'{fun_t.shape} != {self.fun_num}'
            assert prob_t.shape==(self.p_bins,), f'{prob_t.shape} != {self.p_bins}'
            assert mag_t.shape==(self.m_bins,), f'{mag_t.shape} != {self.m_bins}'


            if argmax==True:
                fun_idx = torch.argmax(fun_t).item()
                prob_idx = torch.argmax(prob_t).item() # 0 <= p <= 10
                mag = torch.argmax(mag_t).item() # 0 <= m <= 9
            elif argmax==False:
                # we need these to add up to 1 to be valid pdf's of multinomials
                assert torch.sum(fun_t).isclose(torch.ones(1)), torch.sum(fun_t)
                assert torch.sum(prob_t).isclose(torch.ones(1)), torch.sum(prob_t)
                assert torch.sum(mag_t).isclose(torch.ones(1)), torch.sum(mag_t)

                fun_idx = torch.multinomial(fun_t, 1).item() # 0 <= fun <= self.fun_num-1
                prob_idx = torch.multinomial(prob_t, 1).item() # 0 <= p <= 10
                mag = torch.multinomial(mag_t, 1).item() # 0 <= m <= 9

            function = self.augmentation_space[fun_idx][0]
            prob = prob_idx/(self.p_bins-1)

            indices = (fun_idx, prob_idx, mag)

            # log probability is the sum of the log of the softmax values of the indices 
            # (of fun_t, prob_t, mag_t) that we have chosen
            log_prob = torch.log(fun_t[fun_idx]) + torch.log(prob_t[prob_idx]) + torch.log(mag_t[mag])


        # if probability and magnitude are represented as continuous variables
        else:
            fun_t, prob, mag = operation_tensor.split([self.fun_num, 1, 1])
            prob = prob.item()
            # 0 =< prob =< 1
            mag = mag.item()
            # 0 =< mag =< 9

            # make sure the shape is correct
            assert fun_t.shape==(self.fun_num,), f'{fun_t.shape} != {self.fun_num}'
            
            if argmax==True:
                fun_idx = torch.argmax(fun_t)
            elif argmax==False:
                assert torch.sum(fun_t).isclose(torch.ones(1))
                fun_idx = torch.multinomial(fun_t, 1).item()
            prob = round(prob, 1) # round to nearest first decimal digit
            mag = round(mag) # round to nearest integer
            
        function = self.augmentation_space[fun_idx][0]

        assert 0 <= prob <= 1, prob
        assert 0 <= mag <= self.m_bins-1, (mag, self.m_bins)
        
        # if the image function does not require a magnitude, we set the magnitude to None
        if self.augmentation_space[fun_idx][1] == True: # if the image function has a magnitude
            operation = (function, prob, mag)
        else:
            operation =  (function, prob, None)
        
        if return_log_prob:
            return operation, log_prob
        else:
            return operation
        

    def generate_new_policy(self):
        """
        Generate a new policy which can be fed into an AutoAugment object 
        by calling:
            AutoAugment.subpolicies = policy
        
        Args:
            none
        
        Returns:
            new_policy (list[tuple]):
                        A new policy generated by the controller. It
                        has the form of:
                            [
                            (("Invert", 0.8, None), ("Contrast", 0.2, 6)),
                            (("Rotate", 0.7, 2), ("Invert", 0.8, None)),
                            (("Sharpness", 0.8, 1), ("Sharpness", 0.9, 3)),
                            (("ShearY", 0.5, 8), ("Invert", 0.7, None)),
                            ]
                        This object can be fed into an AutoAUgment object
                        by calling: AutoAugment.subpolicies = policy
        """

        raise NotImplementedError('generate_new_policy not implemented in aa_learner')


    def learn(self, train_dataset, test_dataset, child_network_architecture, iterations=15):
        """
        Runs the main loop (of finding a good policy for the given child network,
        training dataset, and test(validation) dataset)

        Does the loop which is seen in Figure 1 in the AutoAugment paper
        which is:
            1. <generate a random policy>
            2. <see how good that policy is>
            3. <save how good the policy is in a list/dictionary and 
                (if applicable,) update the controller (e.g. RL agent)>
        
        Args:
            train_dataset (torchvision.dataset.vision.VisionDataset)
            test_dataset (torchvision.dataset.vision.VisionDataset)
            child_network_architecture (Union[function, nn.Module]):
                                NOTE This can be both, for example,
                                    MyNetworkArchitecture
                                    and
                                    MyNetworkArchitecture()
            iterations (int): how many different policies do you want to test
        Returns:
            none
        
        
        If child_network_architecture is a <function>, then we make an 
        instance of it. If this is a <nn.Module>, we make a copy.deepcopy
        of it. We make a copy of it because we we want to keep an untrained 
        (initialized but not trained) version of the child network
        architecture, because we need to train it multiple times
        for each policy. Keeping child_network_architecture as a `function` is
        potentially better than keeping it as a nn.Module because every
        time we make a new instance, the weights are differently initialized
        which means that our results will be less biased
        (https://en.wikipedia.org/wiki/Bias_(statistics)).
        

        Example code:

        .. code-block::
            :caption: This is an example dummy code which tests out 15 
                      different policies
            
            for _ in range(15):
                policy = self.generate_new_policy()

                pprint(policy)
                reward = self.test_autoaugment_policy(policy,
                                        child_network_architecture,
                                        train_dataset,
                                        test_dataset)

                self.history.append((policy, reward))
        """
    

    def test_autoaugment_policy(self,
                                policy,
                                child_network_architecture,
                                train_dataset,
                                test_dataset,
                                logging=False,
                                print_every_epoch=True):
        """
        Given a policy (using AutoAugment paper terminology), we train a child network
        using the policy and return the accuracy (how good the policy is for the dataset and 
        child network).

        Args: 
            policy (list[tuple]): A list of tuples representing a policy.
            child_network_architecture (Union[function, nn.Module]):
                                If this is a :code:`function`, then we make
                                an instance of it. If this is a 
                                :code:`nn.Module`, we make a :code:`copy.deepcopy`
                                of it.
            train_dataset (torchvision.dataset.vision.VisionDataset)
            test_dataset (torchvision.dataset.vision.VisionDataset)
            logging (boolean): Whether we want to save logs
        
        Returns:
            accuracy (float): best accuracy reached in any
        """

        
        if isinstance(child_network_architecture, types.FunctionType):
            child_network = child_network_architecture()
        elif isinstance(child_network_architecture, type):
            child_network = child_network_architecture()
        elif isinstance(child_network_architecture, torch.nn.Module):
            child_network = copy.deepcopy(child_network_architecture)
        else:
            raise ValueError('child_network_architecture must either be \
                            a <function> or a <torch.nn.Module>. Type of : ',
                            child_network_architecture, ': ' ,
                            type(child_network_architecture))

        # We need to define an object aa_transform which takes in the image and 
        # transforms it with the policy (specified in its .policies attribute)
        # in its forward pass
        aa_transform = AutoAugment()
        aa_transform.subpolicies = policy
        train_transform = transforms.Compose([
                                                aa_transform,
                                                transforms.ToTensor()
                                            ])
        
        # We feed the transformation into the Dataset object
        train_dataset.transform = train_transform

        # create Dataloader objects out of the Dataset objects
        train_loader, test_loader = create_toy(train_dataset,
                                            test_dataset,
                                            batch_size=self.batch_size,
                                            n_samples=self.toy_size,
                                            seed=100)
        
        # train the child network with the dataloaders equipped with our specific policy
        accuracy = train_child_network(child_network, 
                                    train_loader, 
                                    test_loader, 
                                    sgd = optim.SGD(child_network.parameters(),
                                                    lr=self.learning_rate),
                                    # sgd = optim.Adadelta(
                                    #               child_network.parameters(),
                                    #               lr=self.learning_rate),
                                    cost = nn.CrossEntropyLoss(),
                                    max_epochs = self.max_epochs, 
                                    early_stop_num = self.early_stop_num, 
                                    logging = logging,
                                    print_every_epoch=print_every_epoch)
        
        # if logging is true, 'accuracy' is actually a tuple: (accuracy, accuracy_log)
        return accuracy
    

    # def demo_plot(self, train_dataset, test_dataset, child_network_architecture, n=5):
    #     """
    #     I made this to plot a couple of accuracy graphs to help manually tune my gradient 
    #     optimizer hyperparameters.

    #     Saves a plot of `n` training accuracy graphs overlapped.
    #     """
        
    #     acc_lists = []

    #     # This is dummy code
    #     # test out `n` random policies
    #     for _ in range(n):
    #         policy = self.generate_new_policy()

    #         pprint(policy)
    #         reward, acc_list = self.test_autoaugment_policy(policy,
    #                                             child_network_architecture,
    #                                             train_dataset,
    #                                             test_dataset,
    #                                             logging=True)

    #         self.history.append((policy, reward))
    #         acc_lists.append(acc_list)

    #     for acc_list in acc_lists:
    #         plt.plot(acc_list)
    #     plt.title('I ran 5 random policies to see if there is any sign of \
    #                 catastrophic failure during training. If there are \
    #                 any lines which reach significantly lower (>10%) \
    #                 accuracies, you might want to tune the hyperparameters')
    #     plt.xlabel('epoch')
    #     plt.ylabel('accuracy')
    #     plt.show()
    #     plt.savefig('training_graphs_without_policies')