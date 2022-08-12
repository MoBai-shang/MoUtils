import plotly as py
import plotly.figure_factory as ff
pyplt = py.offline.plot
df = [dict(Task="数据获取", Start='2021-03-01', Finish='2021-03-7', Complete=100),
      dict(Task="数据预处理", Start='2021-03-07', Finish='2021-03-15', Complete=100),
      dict(Task="数据预处理", Start='2021-03-01', Finish='2021-03-17', Complete=100),
      dict(Task="特征工程", Start='2021-03-17', Finish='2021-03-20', Complete=100),
      dict(Task="模型构建", Start='2021-03-20', Finish='2021-03-31', Complete=100),
      dict(Task="性能评估", Start='2021-03-31', Finish='2021-04-08', Complete=100),
      dict(Task="应用分析", Start='2021-04-08', Finish='2021-04-15', Complete=100),
    dict(Task="论文撰写", Start='2021-04-15', Finish='2021-05-15', Complete=5)]
fig = ff.create_gantt(df,  index_col='Complete', show_colorbar=True)
pyplt(fig, filename='1.html')
