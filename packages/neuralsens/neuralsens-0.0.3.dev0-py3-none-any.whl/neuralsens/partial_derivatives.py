import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from neuralsens.activation_functions import activation_function, der_activation_function, der_2_activation_function, der_3_activation_function  
plt.style.use('ggplot')

def jacobian_mlp(wts: list[float], 
                bias: list[float], 
                actfunc: list[str], 
                X: pd.core.frame.DataFrame, 
                y: pd.core.frame.DataFrame, 
                sens_origin_layer: int = 0 , 
                sens_end_layer: str = 'last', 
                sens_origin_input: bool = True, 
                sens_end_input: bool = False):
    ### Initialize all the necessary variables
    # Structure of the mlp model
    mlpstr = [wts[0].shape[0]] + [lyr.shape[1] for lyr in wts] 

    # Derivative and activation functions for each neuron layer
    deractfunc = [der_activation_function(af) for af in actfunc]
    actfunc = [activation_function(af) for af in actfunc]

    # Number of samples to be cached (it is used several times)
    n_samples = X.shape[0]
    r_samples = range(n_samples)
    
    # Weights of input layer
    W = [np.identity(X.shape[1])]

    # Input of input layer 
    # inputs = [np.hstack((np.ones((len(X_train),1), dtype=int), X_train))]
    Z = [np.dot(X, W[0])]

    # Output of input layer
    O = [actfunc[0](Z[0])]

    # Derivative of input layer
    D = [np.array([deractfunc[0](Z[0][irow,]) for irow in r_samples])]

    # Let's go over all the layers calculating each variable
    for lyr in range(1,len(mlpstr)):
        # Calculate weights of each layer
        W.append(np.vstack((bias[lyr-1], wts[lyr-1])))
        
        # Calculate input of each layer
        # Add columns of 1 for the bias
        aux = np.ones((O[lyr-1].shape[0],O[lyr-1].shape[1]+1))
        aux[:,1:] = O[lyr-1]
        Z.append(np.dot(aux,W[lyr]))
        
        # Calculate output of each layer
        O.append(actfunc[lyr](Z[lyr]))
        
        # Calculate derivative of each layer
        D.append(np.array([deractfunc[lyr](Z[lyr][irow,]) for irow in r_samples]))

    # Now, let's calculate the derivatives of interest
    if sens_end_layer == 'last':
        sens_end_layer = len(actfunc)

    warn = ''' 
    if any([sens_end_layer, sens_origin_layer] <= 0):
        pass # Warning explaining that the number of layers should be positive

    if not((sens_end_layer > sens_origin_layer) or ((sens_end_layer == sens_origin_layer) and (sens_origin_input and not sens_end_input))):
        pass # Warning explaining that at least one layer of neurons must exist between end and origin

    if any([sens_end_layer, sens_origin_layer] > len(actfunc)):
        pass # Warning explaining that layers specified could not be found in the model'''

    D_accum = [np.identity(mlpstr[sens_origin_layer]) for irow in r_samples]
    if sens_origin_input:
        D_accum = [D[sens_origin_layer]]

    counter = 0
    # Only perform further operations if origin is not equal to end layer  
    if not (sens_origin_layer == sens_end_layer):
        for layer in range(sens_origin_layer + 1, sens_end_layer):
            counter += 1
            # Calculate the derivatives of the layer based on the previous and the weights
            # if (layer == sens_end_layer) and sens_end_input:
            #     D_accum.append(np.array([np.dot(D_accum[counter - 1][irow,], W[layer][1:,:]) for irow in range(X.shape[0])]))
            # else:
            #     D_accum.append(np.array([np.dot(np.dot(D_accum[counter - 1][irow,], W[layer][1:,]), D[layer][irow,]) for irow in range(X.shape[0])]))
            if (layer == sens_end_layer) and sens_end_input:
                D_accum.append(D_accum[counter - 1] @ W[layer][1:,:])
            else:
                D_accum.append(D_accum[counter - 1] @ W[layer][1:,:] @ D[layer])
    
    # Calculate sensitivity measures for each input and output 
    meanSens = np.mean(D_accum[counter], axis=0)
    stdSens = np.std(D_accum[counter], axis=0)
    meansquareSens = np.mean(np.square(D_accum[counter]), axis=0)
    
    # Store the information extracted from sensitivity analysis
    input_name = X.columns.values.tolist()
    sens = [pd.DataFrame({'mean': meanSens[:,icol], 'std': stdSens[:,icol], 'mean_squared': meansquareSens[:,icol]}, index=input_name) for icol in range(meanSens.shape[1])]
    raw_sens = [pd.DataFrame(D_accum[counter][:,:,out], index=range(X.shape[0]), columns=input_name) for out in range(D_accum[counter].shape[2])]
    
    # Create output name for creating self
    output_name = y.columns.to_list()
    if D_accum[counter].shape[2] > 1:
        output_name =  ['_'.join([y.name, lev]) for lev in y.unique()]
    return Jacobian_mlp(sens, raw_sens, mlpstr, X, input_name, output_name)

# Define self class
class Jacobian_mlp:
    def __init__(self, sens: list, 
                raw_sens: list, 
                mlp_struct: list[int], 
                X: pd.core.frame.DataFrame, 
                input_name: list[str], 
                output_name: list[str]):
        self.__sens = sens
        self.__raw_sens = raw_sens
        self.__mlp_struct = mlp_struct
        self.__X = X
        self.__input_names = input_name
        self.__output_name = output_name
    @property
    def sens(self):
        return self.__sens
    @property
    def raw_sens(self):
        return self.__raw_sens
    @property
    def mlp_struct(self):
        return self.__mlp_struct
    @property
    def X(self):
        return self.__X
    @property
    def input_name(self):
        return self.__input_name
    @property
    def output_name(self):
        return self.__output_name

    def summary(self):
        print("Sensitivity analysis of", str(self.mlp_struct), "MLP network.\n")
        print("Sensitivity measures of each output:\n")
        for out in range(len(self.sens)):
            print("$" + self.output_name[out], "\n")
            print(self.sens[out])
    
    def info(self, n=5):
        print("Sensitivity analysis of", str(self.mlp_struct), "MLP network.\n")
        print(self.X.shape[0],'samples\n')
        print("Sensitivities of each output (only ",min([n,self.raw_sens[0].shape[0]])," first samples):\n", sep = "")
        for out in range(len(self.raw_sens)):
            print("$" + self.output_name[out], "\n")
            print(self.raw_sens[out][:min([n,self.raw_sens[out].shape[0]])])

    def plot(self, type='sens'):
        if type=='sens':
            self.sensitivityPlots()
        elif type=='features':
            self.featurePlots()
        elif type=='time':
            self.timePlots()
        else:
            print('The specifyed type', type, 'is not an accepted plot type.')
    def sensitivityPlots(self):
        
        for out in range(len(self.raw_sens)):
            sens = self.sens[out].sort_values(by='mean_squared')
            raw_sens = self.raw_sens[out]
            # Plot mean-std plot
            _, ax = plt.subplots()
            ax.set_xlim([min(sens['mean']) - 0.2 * max(abs(sens['mean'])), max(sens['mean']) + 0.2 * max(abs(sens['mean']))])
            ax.hlines(y=0, xmin=min(sens['mean']) - 0.2 * max(abs(sens['mean'])), xmax=max(sens['mean']) + 0.2 * max(abs(sens['mean'])), color='blue')
            ax.vlines(x=0, ymin=0, ymax=1, color='blue')
            ax.scatter(x=0, y=0, s=150, c='blue')
            for i, txt in enumerate(sens.index.values.tolist()):
                ax.annotate(txt, xy=(sens['mean'][i], sens['std'][i]),  xycoords='data', va="center", ha="center", fontsize='large',
                        bbox=dict(boxstyle="round", fc="w", ec="gray"))
            ax.set_xlabel('mean(Sens)')
            ax.set_ylabel('std(Sens)')
            ax.plot()

            # Plot variable importance mean_sqaured
            colors = plt.cm.cmap_d['Blues_r'](sens['mean_squared']*0.5/max(sens['mean_squared']))
            ax2 = sens.plot.bar(y='mean_squared', color=colors, legend=False, rot=0)
            ax2.set_xlabel('Input variables')
            ax2.set_ylabel('mean(Sens^2)')
            ax2.plot()

            # Plot density of sensitivities
            ax3 = raw_sens.plot.kde()
            ax3.set_xlabel('Sens')
            ax3.set_ylabel('density(Sens)')
            ax3.plot()
    def featurePlots(self):
        pass
    def timePlots(self):
        pass
    

def hessian_mlp(wts: list[float], 
                bias: list[float], 
                actfunc: list[str], 
                X: pd.core.frame.DataFrame, 
                y: pd.core.frame.DataFrame, 
                sens_origin_layer: int = 0 , 
                sens_end_layer: str = 'last', 
                sens_origin_input: bool = True, 
                sens_end_input: bool = False):
    ### Initialize all the necessary variables
    # Structure of the mlp model
    mlpstr = [wts[0].shape[0]] + [lyr.shape[1] for lyr in wts] 

    # Derivative and activation functions for each neuron layer
    der2actfunc = [der_2_activation_function(af) for af in actfunc]
    deractfunc = [der_activation_function(af) for af in actfunc]
    actfunc = [activation_function(af) for af in actfunc]

    # Number of samples to be cached (it is used several times)
    n_samples = X.shape[0]
    r_samples = range(n_samples)
    n_inputs = X.shape[1]
    
    # Weights of input layer
    W = [np.identity(X.shape[1])]

    # Input of input layer 
    # inputs = [np.hstack((np.ones((len(X_train),1), dtype=int), X_train))]
    Z = [np.dot(X, W[0])]

    # Output of input layer
    O = [actfunc[0](Z[0])]

    # First Derivative of input layer
    D = [np.array([deractfunc[0](Z[0][irow,]) for irow in r_samples])]

    # Second derivative of input layer
    D2 = [np.array([der2actfunc[0](Z[0][irow,]) for irow in r_samples])]

    # Let's go over all the layers calculating each variable
    for lyr in range(1,len(mlpstr)):
        # Calculate weights of each layer
        W.append(np.vstack((bias[lyr-1], wts[lyr-1])))
        
        # Calculate input of each layer
        # Add columns of 1 for the bias
        aux = np.ones((O[lyr-1].shape[0],O[lyr-1].shape[1]+1))
        aux[:,1:] = O[lyr-1]
        Z.append(np.dot(aux,W[lyr]))
        
        # Calculate output of each layer
        O.append(actfunc[lyr](Z[lyr]))
        
        # Calculate first derivative of each layer
        D.append(np.array([deractfunc[lyr](Z[lyr][irow,]) for irow in r_samples]))
        
        # Calculate second derivative of each layer
        D2.append(np.array([der2actfunc[lyr](Z[lyr][irow,]) for irow in r_samples]))
        
    # Now, let's calculate the derivatives of interest
    if sens_end_layer == 'last':
        sens_end_layer = len(actfunc)

    warn = ''' if not all(isinstance([sens_end_layer, sens_origin_layer], numbers.Number)):
        pass # Warning explaining that they should send a number in the layers

    if any([sens_end_layer, sens_origin_layer] <= 0):
        pass # Warning explaining that the number of layers should be positive

    if not((sens_end_layer > sens_origin_layer) or ((sens_end_layer == sens_origin_layer) and (sens_origin_input and not sens_end_input))):
        pass # Warning explaining that at least one layer of neurons must exist between end and origin

    if any([sens_end_layer, sens_origin_layer] > len(actfunc)):
        pass # Warning explaining that layers specified could not be found in the model'''

    # Initialize derivatives
    D_accum = [np.identity(mlpstr[sens_origin_layer]) for irow in r_samples]
    if sens_origin_input:
        D_accum = [D[sens_origin_layer]]
    Q = [np.zeros((n_samples,n_inputs,n_inputs,n_inputs))]
    H = [D2[0]]
    
    counter = 0
    # Only perform further operations if origin is not equal to end layer  
    if not (sens_origin_layer == sens_end_layer):
        for layer in range(sens_origin_layer + 1, sens_end_layer):
            counter += 1 
            # First derivatives
            d_accum = D_accum[counter - 1] @ D[layer-1] @ W[layer][1:,:] 
            
            # Second derivatives
            q = np.matmul(np.matmul(H[counter-1], W[layer][1:,:]).swapaxes(0,1), D[counter]).swapaxes(0,1)
            h = np.matmul(d_accum, np.matmul(d_accum, D2[layer].swapaxes(0,1)).swapaxes(0,2)).swapaxes(0,2).swapaxes(0,1)
            
            # Store results
            D_accum.append(d_accum)
            Q.append(q)
            H.append(h + q)
    
    if sens_end_input:
        raw_sens = Q[counter] 
    else:
        raw_sens = H[counter]
    
    # Calculate sensitivity measures for each input and output 
    meanSens = np.mean(raw_sens, axis=0)
    stdSens = np.std(raw_sens, axis=0)
    meansquareSens = np.mean(np.square(raw_sens), axis=0)
    
    # Store the information extracted from sensitivity analysis
    input_name = X.columns.values.tolist()
    metrics = ['mean', 'std', 'mean_squared']
    
    sens = [pd.DataFrame(np.array([meanSens[:,:,out], stdSens[:,:,out], meansquareSens[:,:,out]]).T.reshape(meanSens.shape[1],-1), 
                        columns=pd.MultiIndex.from_product([metrics,input_name], names=['metric','input']), 
                        index=input_name) for out in range(meanSens.shape[2])]
    
    raw_sens = [pd.DataFrame(raw_sens[:,:,:,out].T.reshape(raw_sens.shape[1]*raw_sens.shape[2],-1).T, 
                            index=range(raw_sens.shape[0]), 
                            columns=pd.MultiIndex.from_product([input_name, input_name], names=['input','input'])) 
                for out in range(raw_sens.shape[3])]
    for out in range(meanSens.shape[2]):
        # Replace values on measures because don't know why they are not ordered correctly
        sens[out]['mean'] = meanSens[:,:,out]
        sens[out]['std'] = stdSens[:,:,out]
        sens[out]['mean_squared'] = meansquareSens[:,:,out]
        
        
    
    # Create output name for creating self
    output_name = y.columns.to_list()
    if D_accum[counter].shape[2] > 1:
        output_name =  ['_'.join([y.name, lev]) for lev in y.unique()]
    return Hessian_mlp(sens, raw_sens, mlpstr, X, input_name, output_name)

# Define self class
class Hessian_mlp:
    def __init__(self, sens: list, 
                raw_sens: list, 
                mlp_struct: list[int], 
                X: pd.core.frame.DataFrame, 
                input_name: list[str], 
                output_name: list[str]):
        self.__sens = sens
        self.__raw_sens = raw_sens
        self.__mlp_struct = mlp_struct
        self.__X = X
        self.__input_names = input_name
        self.__output_name = output_name
    @property
    def sens(self):
        return self.__sens
    @property
    def raw_sens(self):
        return self.__raw_sens
    @property
    def mlp_struct(self):
        return self.__mlp_struct
    @property
    def X(self):
        return self.__X
    @property
    def input_name(self):
        return self.__input_names
    @property
    def output_name(self):
        return self.__output_name

    def summary(self):
        print("Sensitivity analysis of", str(self.mlp_struct), "MLP network.\n")
        print("Sensitivity measures of each output:\n")
        for out in range(len(self.sens)):
            print("$" + self.output_name[out], "\n")
            print(self.sens[out])
    
    def info(self, n=5):
        print("Sensitivity analysis of", str(self.mlp_struct), "MLP network.\n")
        print(self.X.shape[0],'samples\n')
        print("Sensitivities of each output (only ",min([n,self.raw_sens[0].shape[0]])," first samples):\n", sep = "")
        for out in range(len(self.raw_sens)):
            print("$" + self.output_name[out], "\n")
            print(self.raw_sens[out][:min([n,self.raw_sens[out].shape[0]])])

    def plot(self, type='sens'):
        if type=='sens':
            self.sensitivityPlots()
        elif type=='features':
            self.featurePlots()
        elif type=='time':
            self.timePlots()
        else:
            print('The specifyed type', type, 'is not an accepted plot type.')
    def sensitivityPlots(self):
        temp_self = self.hesstosens()
        
        for out in range(len(self.raw_sens)):
            sens = temp_self.sens[out]
            raw_sens = temp_self.raw_sens[out]
            # Plot mean-std plot
            _, ax = plt.subplots()
            ax.set_xlim([min(sens['mean']) - 0.2 * max(abs(sens['mean'])), max(sens['mean']) + 0.2 * max(abs(sens['mean']))])
            ax.hlines(y=0, xmin=min(sens['mean']) - 0.2 * max(abs(sens['mean'])), xmax=max(sens['mean']) + 0.2 * max(abs(sens['mean'])), color='blue')
            ax.vlines(x=0, ymin=0, ymax=1, color='blue')
            ax.scatter(x=0, y=0, s=150, c='blue')
            for i, txt in enumerate(sens.index.values.tolist()):
                ax.annotate(txt, xy=(sens['mean'][i], sens['std'][i]),  xycoords='data', va="center", ha="center", fontsize='large',
                        bbox=dict(boxstyle="round", fc="w", ec="gray"))
            ax.set_xlabel('mean(Sens)')
            ax.set_ylabel('std(Sens)')
            ax.plot()

            # Plot variable importance mean_sqaured
            colors = plt.cm.cmap_d['Blues_r'](sens['mean_squared']*0.5/max(sens['mean_squared']))
            ax2 = sens.plot.bar(y='mean_squared', color=colors, legend=False, rot=0)
            ax2.set_xlabel('Input variables')
            ax2.set_ylabel('mean(Sens^2)')
            ax2.plot()

            # Plot density of sensitivities
            ax3 = raw_sens.plot.kde()
            ax3.set_xlabel('Sens')
            ax3.set_ylabel('density(Sens)')
            ax3.plot()
    def featurePlots(self):
        pass
    def timePlots(self):
        pass
    def hesstosens(self):
        temp_self = self
        for out in range(len(self.raw_sens)):
            n_inputs = len(temp_self.input_name)
            index_of_interest = np.triu_indices(n_inputs)
            mean = temp_self.sens[out]['mean'].to_numpy()[index_of_interest]
            std = temp_self.sens[out]['std'].to_numpy()[index_of_interest]
            mean_squared = temp_self.sens[out]['mean_squared'].to_numpy()[index_of_interest]
            input_names = np.meshgrid(temp_self.input_name, temp_self.input_name)
            input_names = input_names[0].astype(object) + '_' + input_names[1].astype(object)
            input_names = input_names[index_of_interest]
            temp_self.sens[out] =pd.DataFrame({'mean': mean, 'std': std, 'mean_squared': mean_squared}, index=input_names)
            raw_sens = temp_self.raw_sens[out].to_numpy().reshape(temp_self.raw_sens[out].to_numpy().shape[0], n_inputs, n_inputs)            
            raw_sens = np.array([raw_sens[:,x,y] for x,y in zip(index_of_interest[0],index_of_interest[1])])
            temp_self.raw_sens[out] = pd.DataFrame(raw_sens.T, index=range(raw_sens.shape[1]), columns=input_names)
    
        return temp_self
def jerkian_mlp(wts: list[float], 
                bias: list[float], 
                actfunc: list[str], 
                X: pd.core.frame.DataFrame, 
                y: pd.core.frame.DataFrame, 
                sens_origin_layer: int = 0 , 
                sens_end_layer: str = 'last', 
                sens_origin_input: bool = True, 
                sens_end_input: bool = False):
    ### Initialize all the necessary variables
    # Structure of the mlp model
    mlpstr = [wts[0].shape[0]] + [lyr.shape[1] for lyr in wts] 

    # Derivative and activation functions for each neuron layer
    der3actfunc = [der_3_activation_function(af) for af in actfunc]
    der2actfunc = [der_2_activation_function(af) for af in actfunc]
    deractfunc = [der_activation_function(af) for af in actfunc]
    actfunc = [activation_function(af) for af in actfunc]

    # Number of samples to be cached (it is used several times)
    n_samples = X.shape[0]
    r_samples = range(n_samples)
    n_inputs = X.shape[1]

    # Weights of input layer
    W = [np.identity(X.shape[1])]

    # Input of input layer 
    # inputs = [np.hstack((np.ones((len(X_train),1), dtype=int), X_train))]
    Z = [np.dot(X, W[0])]

    # Output of input layer
    O = [actfunc[0](Z[0])]

    # First Derivative of input layer
    D = [np.array([deractfunc[0](Z[0][irow,]) for irow in r_samples])]

    # Second derivative of input layer
    D2 = [np.array([der2actfunc[0](Z[0][irow,]) for irow in r_samples])]

    # Third derivative of input layer
    D3 = [np.array([der3actfunc[0](Z[0][irow,]) for irow in r_samples])]
    
    # Let's go over all the layers calculating each variable
    for lyr in range(1,len(mlpstr)):
        # Calculate weights of each layer
        W.append(np.vstack((bias[lyr-1], wts[lyr-1])))
        
        # Calculate input of each layer
        # Add columns of 1 for the bias
        aux = np.ones((O[lyr-1].shape[0],O[lyr-1].shape[1]+1))
        aux[:,1:] = O[lyr-1]
        Z.append(np.dot(aux,W[lyr]))
        
        # Calculate output of each layer
        O.append(actfunc[lyr](Z[lyr]))
        
        # Calculate first derivative of each layer
        D.append(np.array([deractfunc[lyr](Z[lyr][irow,]) for irow in r_samples]))
        
        # Calculate second derivative of each layer
        D2.append(np.array([der2actfunc[lyr](Z[lyr][irow,]) for irow in r_samples]))
        
        # Calculate third derivative of each layer
        D3.append(np.array([der3actfunc[lyr](Z[lyr][irow,]) for irow in r_samples]))
        
    # Now, let's calculate the derivatives of interest
    if sens_end_layer == 'last':
        sens_end_layer = len(actfunc)

    warn = ''' if not all(isinstance([sens_end_layer, sens_origin_layer], numbers.Number)):
        pass # Warning explaining that they should send a number in the layers

    if any([sens_end_layer, sens_origin_layer] <= 0):
        pass # Warning explaining that the number of layers should be positive

    if not((sens_end_layer > sens_origin_layer) or ((sens_end_layer == sens_origin_layer) and (sens_origin_input and not sens_end_input))):
        pass # Warning explaining that at least one layer of neurons must exist between end and origin

    if any([sens_end_layer, sens_origin_layer] > len(actfunc)):
        pass # Warning explaining that layers specified could not be found in the model'''

    # Initialize cross derivatives
    D_ = [np.identity(mlpstr[sens_origin_layer]) for irow in r_samples]
    if sens_origin_input:
        D_ = [D[sens_origin_layer]]
    Q = [np.zeros((n_samples,n_inputs,n_inputs,n_inputs))]
    H = [D2[0]]

    M = [np.zeros((n_samples,n_inputs,n_inputs,n_inputs,n_inputs))]
    # N = [np.zeros((n_samples,n_inputs,n_inputs,n_inputs,n_inputs))]
    J = [D3[0]]
    
    counter = 0
    for layer in range(sens_origin_layer + 1, sens_end_layer):
        counter += 1

        # First derivatives
        z_ = D_[counter - 1] @ W[layer][1:,:] 
        D_.append(z_ @ D[layer])

        # Second derivatives
        q = np.matmul(np.matmul(H[counter-1], W[layer][1:,:]).swapaxes(0,1), D[counter]).swapaxes(0,1)
        h = np.matmul(z_, np.matmul(z_, D2[layer].swapaxes(0,1)).swapaxes(0,2)).swapaxes(0,1)
        Q.append(q)
        H.append(h + q)

        # Third derivatives
        m = np.matmul(np.matmul(J[counter-1], W[layer][1:,:]).swapaxes(0,2), D[counter]).swapaxes(0,2)
        n = np.matmul(z_,np.matmul(np.matmul(np.broadcast_to(np.expand_dims(q, axis=4), list(q.shape) + [q.shape[-1]]).swapaxes(0,2).swapaxes(0,3),D2[layer][:,:,0,:]).swapaxes(1,3),D2[layer][:,0,:,:]).swapaxes(0,3)).swapaxes(0,2)
        j = np.matmul(z_, np.matmul(z_, np.matmul(z_, D3[layer].swapaxes(0,2)).swapaxes(0,3)).swapaxes(1,3)).swapaxes(0,2)

        M.append(m)
        # N.append(n)
        J.append(j + m + n + n.swapaxes(2, 3).swapaxes(1, 2) + n.swapaxes(1, 2).swapaxes(2, 3))
    
    if sens_end_input:
        raw_sens = M[counter] 
    else:
        raw_sens = J[counter]
    
    # Calculate sensitivity measures for each input and output 
    meanSens = np.mean(raw_sens, axis=0)
    stdSens = np.std(raw_sens, axis=0)
    meansquareSens = np.mean(np.square(raw_sens), axis=0)
    
    # Store the information extracted from sensitivity analysis
    input_name = X.columns.values.tolist()
    metrics = ['mean', 'std', 'mean_squared']
    
    sens = [pd.DataFrame(np.array([meanSens[:,:,out], stdSens[:,:,out], meansquareSens[:,:,out]]).T.reshape(meanSens.shape[1],-1), 
                        columns=pd.MultiIndex.from_product([metrics,input_name], names=['metric','input']), 
                        index=input_name) for out in range(meanSens.shape[2])]
    
    raw_sens = [pd.DataFrame(raw_sens[:,:,:,out].T.reshape(raw_sens.shape[1]*raw_sens.shape[2],-1).T, 
                            index=range(raw_sens.shape[0]), 
                            columns=pd.MultiIndex.from_product([input_name, input_name], names=['input','input'])) 
                for out in range(raw_sens.shape[3])]
    for out in range(meanSens.shape[2]):
        # Replace values on measures because don't know why they are not ordered correctly
        sens[out]['mean'] = meanSens[:,:,out]
        sens[out]['std'] = stdSens[:,:,out]
        sens[out]['mean_squared'] = meansquareSens[:,:,out]
        
        
    
    # Create output name for creating self
    output_name = y.columns.to_list()
    if D_[counter].shape[2] > 1:
        output_name =  ['_'.join([y.name, lev]) for lev in y.unique()]
    return Jerkian_mlp(sens, raw_sens, mlpstr, X, input_name, output_name)

# Define self class
class Jerkian_mlp:
    def __init__(self, sens: list, 
                raw_sens: list, 
                mlp_struct: list[int], 
                X: pd.core.frame.DataFrame, 
                input_name: list[str], 
                output_name: list[str]):
        self.__sens = sens
        self.__raw_sens = raw_sens
        self.__mlp_struct = mlp_struct
        self.__X = X
        self.__input_names = input_name
        self.__output_name = output_name
    @property
    def sens(self):
        return self.__sens
    @property
    def raw_sens(self):
        return self.__raw_sens
    @property
    def mlp_struct(self):
        return self.__mlp_struct
    @property
    def X(self):
        return self.__X
    @property
    def input_name(self):
        return self.__input_names
    @property
    def output_name(self):
        return self.__output_name

    def summary(self):
        print("Sensitivity analysis of", str(self.mlp_struct), "MLP network.\n")
        print("Sensitivity measures of each output:\n")
        for out in range(len(self.sens)):
            print("$" + self.output_name[out], "\n")
            print(self.sens[out])
    
    def info(self, n=5):
        print("Sensitivity analysis of", str(self.mlp_struct), "MLP network.\n")
        print(self.X.shape[0],'samples\n')
        print("Sensitivities of each output (only ",min([n,self.raw_sens[0].shape[0]])," first samples):\n", sep = "")
        for out in range(len(self.raw_sens)):
            print("$" + self.output_name[out], "\n")
            print(self.raw_sens[out][:min([n,self.raw_sens[out].shape[0]])])

    def plot(self, type='sens'):
        if type=='sens':
            self.sensitivityPlots()
        elif type=='features':
            self.featurePlots()
        elif type=='time':
            self.timePlots()
        else:
            print('The specifyed type', type, 'is not an accepted plot type.')
    def sensitivityPlots(self):
        temp_self = self.hesstosens()
        
        for out in range(len(self.raw_sens)):
            sens = temp_self.sens[out]
            raw_sens = temp_self.raw_sens[out]
            # Plot mean-std plot
            _, ax = plt.subplots()
            ax.set_xlim([min(sens['mean']) - 0.2 * max(abs(sens['mean'])), max(sens['mean']) + 0.2 * max(abs(sens['mean']))])
            ax.hlines(y=0, xmin=min(sens['mean']) - 0.2 * max(abs(sens['mean'])), xmax=max(sens['mean']) + 0.2 * max(abs(sens['mean'])), color='blue')
            ax.vlines(x=0, ymin=0, ymax=1, color='blue')
            ax.scatter(x=0, y=0, s=150, c='blue')
            for i, txt in enumerate(sens.index.values.tolist()):
                ax.annotate(txt, xy=(sens['mean'][i], sens['std'][i]),  xycoords='data', va="center", ha="center", fontsize='large',
                        bbox=dict(boxstyle="round", fc="w", ec="gray"))
            ax.set_xlabel('mean(Sens)')
            ax.set_ylabel('std(Sens)')
            ax.plot()

            # Plot variable importance mean_sqaured
            colors = plt.cm.cmap_d['Blues_r'](sens['mean_squared']*0.5/max(sens['mean_squared']))
            ax2 = sens.plot.bar(y='mean_squared', color=colors, legend=False, rot=0)
            ax2.set_xlabel('Input variables')
            ax2.set_ylabel('mean(Sens^2)')
            ax2.plot()

            # Plot density of sensitivities
            ax3 = raw_sens.plot.kde()
            ax3.set_xlabel('Sens')
            ax3.set_ylabel('density(Sens)')
            ax3.plot()
    def featurePlots(self):
        pass
    def timePlots(self):
        pass
    def hesstosens(self):
        temp_self = self
        for out in range(len(self.raw_sens)):
            n_inputs = len(temp_self.input_name)
            index_of_interest = np.triu_indices(n_inputs)
            mean = temp_self.sens[out]['mean'].to_numpy()[index_of_interest]
            std = temp_self.sens[out]['std'].to_numpy()[index_of_interest]
            mean_squared = temp_self.sens[out]['mean_squared'].to_numpy()[index_of_interest]
            input_names = np.meshgrid(temp_self.input_name, temp_self.input_name)
            input_names = input_names[0].astype(object) + '_' + input_names[1].astype(object)
            input_names = input_names[index_of_interest]
            temp_self.sens[out] =pd.DataFrame({'mean': mean, 'std': std, 'mean_squared': mean_squared}, index=input_names)
            raw_sens = temp_self.raw_sens[out].to_numpy().reshape(temp_self.raw_sens[out].to_numpy().shape[0], n_inputs, n_inputs)            
            raw_sens = np.array([raw_sens[:,x,y] for x,y in zip(index_of_interest[0],index_of_interest[1])])
            temp_self.raw_sens[out] = pd.DataFrame(raw_sens.T, index=range(raw_sens.shape[1]), columns=input_names)
    
        return temp_self

def alpha_sens(jacobian:Jacobian_mlp, tol: float = None, ):
    pass

def alpha_curve():
    pass