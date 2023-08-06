from mip import *
import pandas as pd

class MSCCR():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list,un_output_cols: list, vv):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols+un_output_cols
        self.output = output_cols
        self.vv = vv

    def res(self):
        TE = []
        for i in self.K:
            eff_C = self.__CCRmodel(i)
            TE.append(eff_C)
        self.data['CCR超效率值'] = TE
        return self.data[self.input+self.output+['超效率值']]
    
    def __CCRmodel(self, i):
        model = Model(sense=MINIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        sita = model.add_var(var_type=CONTINUOUS, lb=0)
        for p in self.output:
            model += xsum(lambdas[j] * self.data.loc[j,p] for j in self.K if j!= i) - self.data.loc[i,p] >=0
        for q in self.input:
            model += xsum(lambdas[j] * self.data.loc[j,q] for j in self.K if j!= i) - sita * self.data.loc[i,q] <=0
        if self.vv == '规模报酬可变VRS':
            model += xsum(lambdas[j] for j in self.K if j!=i) == 1
        model.objective = sita
        status = model.optimize()
        if status == OptimizationStatus.OPTIMAL:
            eff = sita.x
        else:
            eff = 'INFEASIBLE'
        return eff
    
if __name__ == '__main__':
    data = pd.read_excel(r'deatool\MMODEL\测试数据.xlsx')
    input_cols = ['输入1','输入2']
    output_cols = ['输出1','输出2']
    un_output_cols = ['非期望输出1']
    model = MSCCR(data=data, input_cols = input_cols, output_cols = output_cols,un_output_cols = un_output_cols,vv='规模报酬可变VRS')
    print(model.res())