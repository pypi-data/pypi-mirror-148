### 安装Deatool
- 首先需要您电脑内装有Python，且版本号低于3.9
- 在CMD命令行输入：

    ```cmd
    pip install deatool
    ```
    **由于需要安装相关依赖库，可能需要一段时间，请您耐心等待安装完成**

### 使用Deatool
- 可以选用以下两种方式打开Deatool
2. 在CMD命令行输入：

    ```cmd
    python -m deatool
    ```
3. **[推荐]**直接在CMD命令行输入：
    ```cmd
    deatool
    ```

### Deatool功能介绍
恭喜您已经成功打开了Deatool，接下来将向您介绍这个Python库的功能：
- 计算CCR模型、BCC模型、SBM模型、DDF模型的效率值
- 针对以上模型可以选取不同的规模报酬性，分别是：CRS（constant returns to scale），VRS（variable returns to scale）
- 选择CCR模型，会自动输出CCR、BCC模型下的效率值，并判断规模报酬情况
- 针对DDF模型可以选取不同的方向并设置对非期望产出的处置性
- 针对SBM模型可以输出相应指标的改进量（投入冗余与产出不足）
- 可以处理包含非期望产出的模型
- 可以选取不同的主流处理器，目前支持：Gurobi，Cplex，Glpk，请根据您的求解器安装情况来选取求解器