from mip import *
import pandas as pd
import numpy as np

class MalmSBM:
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, num:int, period:int, vv):
        self.df = data
        self.data = {}
        self.num = num
        self.res = pd.DataFrame()
        self.K = list(range(0,num))
        self.input = input_cols
        self.output = output_cols
        self.period = period
        self.M = list(range(0,len(input_cols)))
        self.N = list(range(0,len(output_cols)))
        self.key = vv
    
    def value(self):
        self.data_pre()
        for t in range(self.period - 1):
            E = []
            T = []
            M = []
            S = []
            PT = []
            for i in self.K:             
                effcrs_1 = self.SBM_model(i, t+1, t+1, 'crs')
                effcrs_2 = self.SBM_model(i, t, t, 'crs') 
                effcrs_3 = self.SBM_model(i, t, t+1, 'crs')
                effcrs_4 = self.SBM_model(i, t+1, t, 'crs')
                EC = effcrs_1/effcrs_2 # 效率变化
                TC = (effcrs_2/effcrs_4 * effcrs_3/effcrs_1)**0.5 # 技术变化
                MI = EC * TC # Malmquist指数
                E.append(EC)
                T.append(TC)
                M.append(MI)
            self.res['effch_{}'.format(t)] = E
            self.res['techch_{}'.format(t)] = T
            self.res['tfpch_{}'.format(t)] = M
        self.res.insert(0, 'DMU',self.df.iloc[0:self.num, 0])
        return self.res
    
    def SBM_model(self, i, r, s, key):
        model = Model(sense=MINIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        slacks_input = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.input}
        slacks_output = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.output}
        t =  model.add_var(var_type=CONTINUOUS, lb=0)
        for p in self.input:
            model += xsum(lambdas[j] * self.data[r].loc[j,p] for j in self.K) + slacks_input[p] -  t * self.data[s].loc[i,p] == 0
        for q in self.output:
            model += xsum(lambdas[j] * self.data[r].loc[j,q] for j in self.K) - slacks_output[q]-  t * self.data[s].loc[i,q] == 0
        model += t + (1/len(self.output)) * xsum(slacks_output[q] / self.data[s].loc[i,q] for q in self.output) == 1
        if self.key == '规模报酬可变VRS':
            model += xsum(lambdas[j] for j in self.K) == t
        model.objective = t - 1/len(self.input) * xsum(slacks_input[p] / self.data[s].loc[i,p] for p in self.input)
        status = model.optimize()
        if status == OptimizationStatus.OPTIMAL:
            eff = model.objective.x
        else:
            eff=self.SBM_model_super(i, r, s, key)
        return eff
        
    def SBM_model_super(self, i, r, s, key):
        model = Model(sense=MINIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        slacks_input = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.input}
        slacks_output = {i: model.add_var(var_type=CONTINUOUS, lb=0) for i in self.output}
        t =  model.add_var(var_type=CONTINUOUS, lb=0)
        for p in self.input:
            model += xsum(lambdas[j] * self.data[r].loc[j,p] for j in self.K if j!=i) - slacks_input[p] -  t * self.data[s].loc[i,p] <= 0
        for q in self.output:
            model += xsum(lambdas[j] * self.data[r].loc[j,q] for j in self.K if j!=i) + slacks_output[q] - t * self.data[s].loc[i,q] >= 0
        model += t - (1/len(self.output)) * xsum(slacks_output[q] / self.data[s].loc[i,q] for q in self.output) == 1
        if self.key == '规模报酬可变VRS':
            model += xsum(lambdas[j] for j in self.K) == t
        model.objective = t + 1/len(self.input) * xsum(slacks_input[p] / self.data[s].loc[i,p] for p in self.input)
        model.optimize()
        eff = model.objective.x
        return eff
         
    def data_pre(self):
        for i in range(self.period):
            self.data[i] = self.df.loc[self.num*i: self.num*(i+1)-1, :].reset_index(drop=True) 
            
if __name__ == '__main__':
    data = pd.read_excel(r'deatool\MMODEL\测试数据.xlsx')
    input_cols = ['输入1','输入2']
    output_cols = ['输出1','输出2']
    DMU = 6
    period = 3
    model = MalmSBM(data=data, input_cols = input_cols, output_cols = output_cols, num = DMU, period = period, vv ='规模报酬可变VRS')
    print(model.value())