from mip import *
import pandas as pd
from numpy import inf

class MSDDF():
    def __init__(self, data: pd.DataFrame, input_cols: list, output_cols: list, un_output_cols: list, dd,vv):
        self.data = data
        self.K = list(range(0,data.shape[0]))
        self.input = input_cols
        self.output = output_cols
        self.unoutput = un_output_cols
        self.dd = dd
        self.vv = vv
        
    def res(self):
        TE = []
        for i in self.K:
            eff = self.__DDFmodel(i,self.data)
            TE.append(eff)
        self.data['DDF超效率值'] = TE
        return self.data[[self.data.columns.values[0]]+self.input+self.output+self.unoutput+['DDF超效率值']]
    
    def __DDFmodel(self, i,data):
        model = Model(sense=MAXIMIZE, solver_name=CBC)
        lambdas = [model.add_var(var_type=CONTINUOUS, lb=0) for i in self.K]
        beta = model.add_var(var_type=CONTINUOUS, lb=-inf)
        for p in self.input:
            model += xsum(lambdas[j] * data.loc[j,p] for j in self.K if j!=i) <= (1-beta) * data.loc[i,p]
        for q in self.output:
            model += xsum(lambdas[j] * data.loc[j,q] for j in self.K if j!=i) >= (1+beta) * data.loc[i,q]
        if self.unoutput!= []:
            if self.dd == '(-x,y,-b)弱可处置性=':
                for u in self.unoutput:
                    model += xsum(lambdas[j] * data.loc[j,u] for j in self.K if j!=i) == (1-beta) * data.loc[i,u]
            elif self.dd == '(-x,y,-b)强可处置性>=':
                for u in self.unoutput:
                    model += xsum(lambdas[j] * data.loc[j,u] for j in self.K if j!=i) >= (1-beta) * data.loc[i,u]
            elif self.dd == '(-x,y,b)强可处置性<=':
                for u in self.unoutput:
                    model += xsum(lambdas[j] * data.loc[j,u] for j in self.K if j!=i) <= (1+beta) * data.loc[i,u]
        if self.vv == '规模报酬可变VRS':
            model += xsum(lambdas[j] for j in self.K if j!=i) == 1
        model.objective = beta
        status = model.optimize()
        if status == OptimizationStatus.INFEASIBLE:
            return 'INFEASIBLE'
        eff = beta.x
        if status == OptimizationStatus.OPTIMAL:
            return eff

if __name__ == '__main__':
    data = pd.read_excel(r'deatool\MMODEL\测试数据.xlsx')
    input_cols = ['输入1','输入2']
    output_cols = ['输出1','输出2']
    un_output_cols = ['非期望输出1']
    model = MSDDF(data=data, input_cols = input_cols, output_cols = output_cols,un_output_cols = un_output_cols, dd= '(-x,y,-b)弱可处置性=', vv='规模报酬可变VRS')
    print(model.res())