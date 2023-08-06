from mip import *
import pandas as pd
import numpy as np

class MalmCCR:
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
                effcrs_1 = self.CCR_model(i, t, t+1, 'crs')
                effcrs_2 = self.CCR_model(i, t, t, 'crs')
                effcrs_3 = self.CCR_model(i, t+1, t, 'crs')
                effcrs_4 = self.CCR_model(i, t+1, t+1, 'crs')
                effvrs_2 = self.CCR_model(i, t, t, 'vrs')
                effvrs_4 = self.CCR_model(i, t+1, t+1, 'vrs')
                EC = effcrs_4/effcrs_2 # 效率变化
                PTE = effvrs_4/effvrs_2 # 纯技术效率变动
                SE = EC/PTE # 规模效率变动
                TC = (effcrs_2/effcrs_3 * effcrs_1/effcrs_4)**0.5 # 技术变化
                MI = EC * TC # Malmquist指数
                E.append(EC)
                T.append(TC)
                M.append(MI)
                PT.append(PTE)
                S.append(SE)
            self.res['effch_period{}'.format(t)] = E
            self.res['techch_period{}'.format(t)] = T
            self.res['pech_period{}'.format(t)] = PT
            self.res['sech_period{}'.format(t)] = S
            self.res['tfpch_period{}'.format(t)] = M
        self.res.insert(0, 'DMU',self.df.iloc[0:self.num, 0])
        return self.res
    
    def CCR_model(self, i, r, t, key):
        model = Model(sense=MINIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        sita = model.add_var(var_type=CONTINUOUS, lb=0)
        for p in self.output:
            model += xsum(lambdas[j] * self.data[r].loc[j,p] for j in self.K) - self.data[t].loc[i,p] >=0
        for q in self.input:
            model += xsum(lambdas[j] * self.data[r].loc[j,q] for j in self.K) - sita * self.data[t].loc[i,q] <=0
        if key == '规模报酬可变VRS':
            model += xsum(lambdas[j] for j in self.K) == 1
        model.objective = sita
        status = model.optimize()
        eff = sita.x
        if status == OptimizationStatus.INFEASIBLE:
            return 'INFEASIBLE'
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
    model = MalmCCR(data=data, input_cols = input_cols, output_cols = output_cols, num = DMU, period = period, vv ='规模报酬不变CRS')
    print(model.value())