from mip import *
import pandas as pd
import numpy as np

class MSSBM():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, un_output_cols: list,vv):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols
        self.output = output_cols
        self.undes = un_output_cols
        self.vv = vv
        
    def res(self):
        if self.undes == []:
            return self.ress()
        else:
            return self.ress_u()
        
    def ress_u(self):
        efficiencies_SBM_model, x_slacks, y_slacks, u_slacks = self.__SBMmodel_u(self.data)
        df_1 = pd.DataFrame(x_slacks)
        df_2 = pd.DataFrame(y_slacks)
        df_3 = pd.DataFrame(u_slacks)
        df = pd.concat([df_1,df_2,df_3],axis=1)
        df.insert(0,'DMU',self.data.iloc[:,0])
        df.insert(1,'效率',efficiencies_SBM_model)    
        return df
    
    def ress(self):
        efficiencies_SBM_model, x_slacks, y_slacks = self.__SBM_model(self.data)
        df_1 = pd.DataFrame(x_slacks)
        df_2 = pd.DataFrame(y_slacks)
        df = pd.concat([df_1,df_2],axis=1)
        df.insert(0,'DMU',self.data.iloc[:,0])
        df.insert(1,'效率',efficiencies_SBM_model)
        return df
    
    def __SBMmodel_u(self, data):
        efficiencies_SBM_model=[]
        x_slacks = {p+'_slacks': [] for p in self.input}
        y_slacks= {q+'_slacks': [] for q in self.output}
        u_slacks = {u+'_slacks': [] for u in self.undes}
        for i in self.K:
            model = Model(sense=MINIMIZE, solver_name=CBC)
            lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
            slacks_input = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.input}
            slacks_output = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.output}
            slacks_undes = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.undes}
            t =  model.add_var(var_type=CONTINUOUS, lb=0)
            for p in self.input:
                model += xsum(lambdas[j] * data.loc[j,p] for j in self.K) +slacks_input[p] -  t * data.loc[i,p] == 0
            for q in self.output:
                model += xsum(lambdas[j] * data.loc[j,q] for j in self.K) - slacks_output[q]-  t * data.loc[i,q] == 0
            for u in self.undes:
                model += xsum(lambdas[j] * data.loc[j,u] for j in self.K) + slacks_undes[u]-  t * data.loc[i,u] == 0
            model += t + 1/(len(self.output)+ len(self.undes))* (xsum(slacks_output[q] / data.loc[i,q] for q in self.output) + xsum(slacks_undes[u] / data.loc[i,u] for u in self.undes)) == 1
            if self.vv == '规模报酬可变VRS':
                model += xsum(lambdas[j] for j in self.K if j!=i) == t
            model.objective = t - 1/len(self.input) * xsum(slacks_input[p] / data.loc[i,p] for p in self.input)
            status = model.optimize()
            if status == OptimizationStatus.OPTIMAL:
                eff = model.objective.x
                x_slack = {p: slacks_input[p].x / t.x if np.abs(slacks_input[p].x / t.x) >= 1e-7 else 0 for p in self.input}
                y_slack = {q: slacks_output[q].x / t.x if np.abs(slacks_output[q].x / t.x) >= 1e-7 else 0 for q in self.output}
                u_slack = {u: slacks_undes[u].x / t.x if np.abs(slacks_undes[u].x / t.x) >= 1e-7 else 0 for u in self.undes}
                if abs(eff-1) <= 0.001:
                    model = Model(sense=MINIMIZE, solver_name=CBC)
                    lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
                    slacks_input = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.input}
                    slacks_output = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.output}
                    slacks_undes = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.undes}
                    t =  model.add_var(var_type=CONTINUOUS, lb=0)
                    for p in self.input:
                        model += xsum(lambdas[j] * data.loc[j,p] for j in self.K if j!=i) - slacks_input[p] -  t * data.loc[i,p] <= 0
                    for q in self.output:
                        model += xsum(lambdas[j] * data.loc[j,q] for j in self.K if j!=i) + slacks_output[q]-  t * data.loc[i,q] >= 0
                    for u in self.undes:
                        model += xsum(lambdas[j] * data.loc[j,u] for j in self.K if j!=i) - slacks_undes[u]-  t * data.loc[i,u] <= 0
                    model += t - 1/(len(self.output)+ len(self.undes))* (xsum(slacks_output[q] / data.loc[i,q] for q in self.output) + xsum(slacks_undes[u] / data.loc[i,u] for u in self.undes)) == 1
                    if self.vv == '规模报酬可变VRS':
                        model += xsum(lambdas[j] for j in self.K if j!=i) == t
                    model.objective = t + 1/len(self.input) * xsum(slacks_input[p] / data.loc[i,p] for p in self.input)
                    model.optimize()
                    eff = model.objective.x
                    x_slack = {p: -slacks_input[p].x / t.x if np.abs(slacks_input[p].x / t.x) >= 1e-7 else 0 for p in self.input}
                    y_slack = {q: -slacks_output[q].x / t.x if np.abs(slacks_output[q].x / t.x) >= 1e-7 else 0 for q in self.output}
                    u_slack = {u: -slacks_undes[u].x / t.x if np.abs(slacks_undes[u].x / t.x) >= 1e-7 else 0 for u in self.undes}
            else:
                eff = 'INFEASIBLE'
                x_slack = {p: 'INFEASIBLE' for p in self.input}
                y_slack = {q: 'INFEASIBLE' for q in self.output}
                u_slack = {u: 'INFEASIBLE' for u in self.undes}
            for s_input in self.input:
                x_slacks[s_input+'_slacks'].append(x_slack[s_input])
            for s_output in self.output:
                y_slacks[s_output+'_slacks'].append(y_slack[s_output])
            for s_undes in self.undes:
                u_slacks[s_undes+'_slacks'].append(u_slack[s_undes])
            efficiencies_SBM_model.append(eff) 
        return efficiencies_SBM_model, x_slacks, y_slacks, u_slacks
    
    def __SBM_model(self,data):
        efficiencies_SBM_model=[]
        x_slacks = {i+'_slacks': [] for i in self.input}
        y_slacks= {j+'_slacks': [] for j in self.output}
        for i in self.K:
            model = Model(sense=MINIMIZE, solver_name=CBC)
            lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
            slacks_input = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.input}
            slacks_output = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.output}
            t =  model.add_var(var_type=CONTINUOUS, lb=0)
            for p in self.input:
                model += xsum(lambdas[j] * data.loc[j,p] for j in self.K) + slacks_input[p] -  t * data.loc[i,p] == 0
            for q in self.output:
                model += xsum(lambdas[j] * data.loc[j,q] for j in self.K) - slacks_output[q]-  t * data.loc[i,q] == 0
            model += t + (1/len(self.output)) * xsum(slacks_output[q] / data.loc[i,q] for q in self.output) == 1
            if self.vv == '规模报酬可变VRS':
                model += xsum(lambdas[j] for j in self.K if j!=i) == t
            model.objective = t - 1/len(self.input) * xsum(slacks_input[p] / data.loc[i,p] for p in self.input)
            status = model.optimize()
            if status == OptimizationStatus.OPTIMAL:
                eff = model.objective.x
                x_slack = {p: slacks_input[p].x / t.x if np.abs(slacks_input[p].x / t.x) >= 1e-7 else 0 for p in self.input}
                y_slack = {q: slacks_output[q].x / t.x if np.abs(slacks_output[q].x / t.x) >= 1e-7 else 0 for q in self.output}
                if abs(eff-1) <= 0.001:
                    model = Model(sense=MINIMIZE, solver_name=CBC)
                    lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
                    slacks_input = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.input}
                    slacks_output = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.output}
                    t =  model.add_var(var_type=CONTINUOUS, lb=0)
                    for p in self.input:
                        model += xsum(lambdas[j] * data.loc[j,p] for j in self.K if j!=i) - slacks_input[p] -  t * data.loc[i,p] <= 0
                    for q in self.output:
                        model += xsum(lambdas[j] * data.loc[j,q] for j in self.K if j!=i) + slacks_output[q] - t * data.loc[i,q] >= 0
                    model += t - (1/len(self.output)) * xsum(slacks_output[q] / data.loc[i,q] for q in self.output) == 1
                    if self.vv == '规模报酬可变VRS':
                        model += xsum(lambdas[j] for j in self.K if j!=i) == t
                    model.objective = t + 1/len(self.input) * xsum(slacks_input[p] / data.loc[i,p] for p in self.input)
                    status = model.optimize()
                    if status == OptimizationStatus.OPTIMAL:
                        eff = model.objective.x
                        x_slack = {p: -slacks_input[p].x / t.x if np.abs(slacks_input[p].x / t.x) >= 1e-7 else 0 for p in self.input}
                        y_slack = {q: -slacks_output[q].x / t.x if np.abs(slacks_output[q].x / t.x) >= 1e-7 else 0 for q in self.output}
            else:
                eff = 'INFEASIBLE'
                x_slack = {p: 'INFEASIBLE' for p in self.input}
                y_slack = {q: 'INFEASIBLE' for q in self.output}
                u_slack = {u: 'INFEASIBLE' for u in self.undes}       
            for s_input in self.input:
                x_slacks[s_input+'_slacks'].append(x_slack[s_input])
            for s_output in self.output:
                y_slacks[s_output+'_slacks'].append(y_slack[s_output])       
            efficiencies_SBM_model.append(eff) 
        return efficiencies_SBM_model, x_slacks, y_slacks

if __name__ == '__main__':
    data = pd.read_excel(r'deatool\MMODEL\测试数据.xlsx')
    input_cols = ['输入1','输入2']
    output_cols = ['输出1','输出2']
    un_output_cols = ['非期望输出1']
    model = MSSBM(data=data, input_cols = input_cols, output_cols = output_cols,un_output_cols = un_output_cols,vv='规模报酬可变VRS')
    print(model.res())