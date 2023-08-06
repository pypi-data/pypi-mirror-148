from mip import *
import pandas as pd

class MCCR():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list,un_output_cols: list, vv):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols+un_output_cols
        self.output = output_cols

    def res(self):
        TE = []
        PTE = []
        SE = []
        Type = []
        for i in self.K:
            eff_B = self.__BCCmodel(i)
            eff_C, Types = self.__CCRmodel(i, eff_B)
            eff_S = eff_C/eff_B
            TE.append(eff_C)
            PTE.append(eff_B)
            SE.append(eff_S)
            Type.append(Types)
        self.data['TE'] = TE
        self.data['PTE'] = PTE
        self.data['SE'] = SE
        self.data['规模报酬分析'] = Type
        return self.data[[self.data.columns.values[0]]+self.input+self.output+['TE','PTE','SE','规模报酬分析']]
    
    def __CCRmodel(self, i, eff_B):
        model = Model(sense=MINIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        sita = model.add_var(var_type=CONTINUOUS, lb=0)
        for p in self.output:
            model += xsum(lambdas[j] * self.data.loc[j,p] for j in self.K) - self.data.loc[i,p] >=0
        for q in self.input:
            model += xsum(lambdas[j] * self.data.loc[j,q] for j in self.K) - sita * self.data.loc[i,q] <=0
        model.objective = sita
        model.optimize()
        eff = sita.x
        Type = 'CRS' if eff_B ==1 else 'IRS' if sum(lambdas[j].x for j in self.K) < 1 and eff<1 else 'DRS'
        return eff, Type
    
    def __BCCmodel(self, i):
        model = Model(sense=MINIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        sita = model.add_var(var_type=CONTINUOUS, lb=0)
        constraints = []
        for p in self.output:
            model += xsum(lambdas[j] * self.data.loc[j,p] for j in self.K) - self.data.loc[i,p] >=0
        for q in self.input:
            model += xsum(lambdas[j] * self.data.loc[j,q] for j in self.K) - sita * self.data.loc[i,q] <=0
        model += xsum(lambdas[j] for j in self.K) == 1
        model.objective = sita
        model.optimize()
        eff = sita.x
        return eff

if __name__ == '__main__':
    data = pd.read_excel(r'deatool\MMODEL\测试数据.xlsx')
    input_cols = ['输入1','输入2']
    output_cols = ['输出1','输出2']
    un_output_cols = ['非期望输出1']
    model = MCCR(data=data, input_cols = input_cols, output_cols = output_cols,un_output_cols = un_output_cols, vv = 1)
    print(model.res())