# Financial Statement Modeling 财务报表建模笔记

> 来源：`22.Financial Statement Modeling _.doc`  
> 主题：财务报表建模、利润表预测、收入预测、成本预测、费用预测、利息费用预测

---

## 一、报表建模的核心含义

Financial Statement Modeling，即**财务报表建模**，指的是根据公司当年的财务报表，对未来年度的财务报表进行预测。

它的核心目的不是简单预测一个现金流增长率，而是通过预测未来的利润表、资产负债表，再进一步推导出未来现金流，为后续股票估值和公司估值服务。

在实务中，如果只是简单假设：

> 今年现金流 = 100 万  
> 明年增长率 = 5%  
> 明年现金流 = 105 万

这种方法过于粗放，缺乏说服力。更加专业的方法是：

```text
先预测未来利润表
再预测未来资产负债表
最后根据利润表和资产负债表推导现金流和自由现金流
```

---

## 二、本章内容框架

本章主要包括三部分内容：

1. **报表预测方法**
   - 先预测利润表
   - 再预测资产负债表
   - 最后计算现金流和自由现金流

2. **报表预测中需要考虑的问题**
   - 行业分析
   - 波特五力模型
   - 通胀变化的影响
   - 科技变化的影响
   - 预测期的确定

3. **行为金融学对报表预测的影响**
   - 投资者或分析师在预测过程中可能受到主观心理偏差影响
   - 需要识别并控制 behavioral bias 对预测结果的干扰

---

## 三、财务报表预测的基本顺序

财务报表预测的顺序非常重要：

```text
先预测利润表
      ↓
再预测资产负债表
      ↓
最后计算现金流量表和自由现金流
```

原因是：

资产负债表中的很多项目需要基于利润表数据进行预测，因此必须先有利润表，才能进一步预测资产负债表。

---

## 四、利润表的基本结构

CFA 中常见的利润表结构如下：

```text
Revenue 营业收入
- COGS 营业成本
= Gross Profit 毛利

- SG&A / Operating Expense 销售费用和管理费用
= Operating Profit / EBIT 经营利润 / 息税前利润

- Interest Expense 利息费用
= EBT 税前利润

- Tax Expense 所得税费用
= Net Income 净利润
```

---

## 五、利润表中真正需要预测的项目

利润表中的各层利润通常不需要单独预测，因为它们可以通过其他项目计算出来。

真正需要预测的项目主要有五个：

| 序号 | 需要预测的项目 | 中文含义 |
|---|---|---|
| 1 | Revenue | 营业收入 |
| 2 | COGS | 营业成本 |
| 3 | SG&A | 销售费用和管理费用 |
| 4 | Interest Expense | 利息费用 |
| 5 | Tax Expense | 所得税费用 |

其中：

```text
Gross Profit = Revenue - COGS
EBIT = Gross Profit - SG&A
EBT = EBIT - Interest Expense
Net Income = EBT - Tax Expense
```

---

# 六、Revenue 营业收入预测

## 1. 为什么 Revenue 最重要？

Revenue 是利润表预测中最核心的项目。

原因是：

- COGS 通常基于 Revenue 推导
- SG&A 中的可变费用通常和 Revenue 相关
- 后续资产负债表项目也会受到 Revenue 影响
- Revenue 预测不准，后面所有项目都会出现偏差

因此，收入预测是整个三大报表预测的起点和核心。

---

## 2. 报表预测的三种方法

| 方法 | 英文 | 含义 |
|---|---|---|
| 自下而上 | Bottom-up Approach | 从公司自身历史数据出发进行预测 |
| 自上而下 | Top-down Approach | 从宏观经济、行业、公司市场份额出发进行预测 |
| 混合方法 | Hybrid Approach | 结合 bottom-up 和 top-down，是实务中最常用的方法 |

---

## 3. Top-down 方法预测 Revenue

自上而下预测收入，通常从三个层面出发：

```text
宏观经济增长
      ↓
行业增长
      ↓
公司市场份额变化
      ↓
公司收入增长
```

### 具体因素

| 层面 | 影响因素 | 说明 |
|---|---|---|
| 宏观层面 | GDP 增长率 | 整体经济增长会带动公司收入自然增长 |
| 行业层面 | 行业增长率 | 朝阳行业或政策支持行业可能增长快于 GDP |
| 公司层面 | 市场份额变化 | 公司市场份额提升会推动收入进一步增长 |

### 基本逻辑

如果公司去年收入为 `Revenue₀`，预测增长率为 `g`，则：

```text
Revenue₁ = Revenue₀ × (1 + g)
```

这里的 `g` 可以综合考虑：

```text
GDP 增长率 + 行业增长率 + 市场份额增长率
```

---

## 4. Bottom-up 方法预测 Revenue

自下而上预测收入，主要基于公司自身历史数据。

最常见的方法是：

> 时间序列模型 Time Series Model

### 核心思路

通过公司历史收入数据，建立当前收入与过去收入之间的关系，再用历史趋势预测未来收入。

```text
根据过去多年的 Revenue 数据
      ↓
建立时间序列或回归模型
      ↓
预测未来年度 Revenue
```

这种方法不直接考虑宏观经济和行业环境，而是完全基于公司自身历史表现。

---

## 5. 特殊行业的 Revenue 预测方法

除了 top-down 和 time series 方法，一些特殊行业还会使用特殊指标进行收入预测。

### 1）银行业：Return on Capital 方法

银行的收入主要来自利息净收入。

银行的核心业务是：

```text
吸收存款
发放贷款
赚取存贷款利差
```

因此银行收入预测通常基于：

```text
贷款资产 × 贷款利率 - 存款负债 × 存款利率
```

也可以理解为基于银行生息资产和市场利率来预测利息净收入。

---

### 2）零售行业：Capacity-based Measure 方法

对于连锁零售、餐饮、咖啡店、奶茶店、服装品牌等行业，收入和门店数量高度相关。

常见方法包括：

| 方法 | 含义 |
|---|---|
| Same-store sales growth | 同店销售增长率 |
| New store contribution | 新店收入贡献 |
| Store count analysis | 门店数量分析 |

### 基本逻辑

```text
老店收入增长
+
新店收入贡献
=
总收入增长
```

对于新开门店，可以参考历史上老店在开业初期的收入表现进行预测。

---

# 七、COGS 营业成本预测

## 1. COGS 的基本预测逻辑

COGS 通常基于 Revenue 和 Gross Margin 推导。

公式为：

```text
Gross Margin = (Revenue - COGS) / Revenue
```

因此：

```text
COGS = Revenue × (1 - Gross Margin)
```

也就是说，只要预测出：

1. Revenue
2. Gross Margin

就可以推导出 COGS。

---

## 2. Gross Margin 如何预测？

通常假设：

> 如果公司经营模式和商业模式没有发生重大变化，毛利率会保持相对稳定。

因此可以参考：

- 过去 5 年平均毛利率
- 过去 10 年平均毛利率
- 最近年度毛利率趋势

---

## 3. 提高 COGS 预测精度的三个方法

### 1）按业务板块或产品线预测

如果公司业务多元化，不同产品或业务板块的毛利率可能差异很大。

例如：

- 高毛利业务
- 低毛利业务
- 成熟产品
- 新兴产品

此时可以采用：

```text
分业务板块预测 COGS
或
分产品线预测 COGS
```

最后再汇总得到总 COGS。

---

### 2）考虑规模效应

规模效应指的是：

> 公司收入规模扩大时，由于固定成本不随收入同比例上升，毛利率可能逐步提高。

例如：

```text
收入增长 10%
成本可能只增长 5% 或 7%
```

因此，如果公司规模持续扩大，可以在历史毛利率基础上适当上调未来毛利率。

例如：

```text
历史平均毛利率 = 40%
考虑规模效应后，未来毛利率可假设为 41% 或 42%
```

---

### 3）考虑成本风险对冲策略

一些公司会通过衍生品或经营策略对冲成本波动风险。

例如：

- 原材料价格对冲
- 大宗商品价格对冲
- 逐步调价策略
- 销售价格调整策略

这些都会影响未来成本水平和毛利率预测。

---

# 八、SG&A 销售费用和管理费用预测

## 1. SG&A 的分类

SG&A 可以分为两类：

| 类型 | 英文 | 特点 |
|---|---|---|
| 固定费用 | Fixed Expense | 与收入规模关系不大 |
| 可变费用 | Variable Expense | 与收入规模高度相关 |

---

## 2. 固定费用预测

固定费用通常与收入增长关系不大，可以假设保持稳定。

例如：

- 部分管理费用
- 部分研发费用
- 办公费用
- 固定行政开支

预测时可以假设：

```text
未来固定费用 ≈ 当前固定费用
```

---

## 3. 可变费用预测

可变费用通常和 Revenue 高度相关，尤其是销售费用。

例如：

- 营销费用
- 推广费用
- 销售人员佣金
- 渠道费用

预测时可以假设：

```text
可变费用增长率 ≈ Revenue 增长率
```

例如：

```text
Revenue 增长 10%
Selling Expense 也增长 10%
```

---

## 4. SG&A 总体预测方法

```text
SG&A = 固定费用 + 可变费用
```

其中：

```text
固定费用：保持稳定
可变费用：跟随收入同比例增长
```

---

# 九、Interest Expense 利息费用预测

## 1. 利息费用的本质

利润表中的 Interest Expense 通常指的是净利息费用。

```text
Net Interest Expense = Interest Expense - Interest Income
```

也就是说，需要分别预测：

1. 利息费用
2. 利息收入

---

## 2. 利息费用预测

利息费用主要来自公司的有息债务。

```text
Interest Expense = Debt × Borrowing Rate
```

其中：

- Debt：公司债务规模
- Borrowing Rate：债务融资利率

---

## 3. 利息收入预测

利息收入主要来自公司的生息资产。

例如：

- 现金
- 现金等价物
- 短期投资
- 短期债券
- 银行存款

公式为：

```text
Interest Income = Cash and Short-term Investments × Deposit Rate
```

---

## 4. 为什么利息费用和利息收入不能用同一个利率？

因为二者对应的资产负债性质不同：

| 项目 | 对应资产/负债 | 常用利率 |
|---|---|---|
| 利息费用 | 长期债务、贷款 | 长期贷款利率 |
| 利息收入 | 现金、短期投资 | 短期存款利率 |

通常：

```text
贷款利率 > 存款利率
```

因此，利息费用率通常显著高于利息收入率。

---

## 5. 净利息费用预测公式

```text
Gross Interest Expense = Gross Debt × Debt Interest Rate

Interest Income = Cash and Short-term Investments × Short-term Interest Rate

Net Interest Expense = Gross Interest Expense - Interest Income
```

---

# 十、Tax Expense 所得税费用预测

讲义在当前内容中只引入了所得税费用预测，具体展开部分尚未完整出现。

一般逻辑是：

```text
Tax Expense = EBT × Effective Tax Rate
```

其中：

- EBT 是税前利润
- Effective Tax Rate 是有效税率

在实务中，预测所得税费用时通常需要考虑：

- 公司历史有效税率
- 法定税率
- 税收优惠政策
- 递延所得税
- 不同地区税率差异

---

# 十一、利润表预测的完整流程

```text
第一步：预测 Revenue
      ↓
第二步：预测 Gross Margin
      ↓
第三步：计算 COGS
      ↓
第四步：计算 Gross Profit
      ↓
第五步：预测 SG&A
      ↓
第六步：计算 EBIT
      ↓
第七步：预测 Net Interest Expense
      ↓
第八步：计算 EBT
      ↓
第九步：预测 Tax Expense
      ↓
第十步：计算 Net Income
```

---

# 十二、核心公式汇总

| 公式 | 含义 |
|---|---|
| `Gross Profit = Revenue - COGS` | 毛利 |
| `Gross Margin = Gross Profit / Revenue` | 毛利率 |
| `COGS = Revenue × (1 - Gross Margin)` | 营业成本 |
| `EBIT = Gross Profit - SG&A` | 息税前利润 |
| `EBT = EBIT - Net Interest Expense` | 税前利润 |
| `Net Income = EBT - Tax Expense` | 净利润 |
| `Net Interest Expense = Interest Expense - Interest Income` | 净利息费用 |

---

# 十三、考试与实务理解重点

## 1. 考试重点

CFA 考试中不会要求考生完整搭建 Excel 财务模型，因为考试形式主要是选择题。

但需要理解：

- 报表预测的基本顺序
- 利润表哪些项目需要预测
- Revenue 为什么最重要
- Revenue 的几种预测方法
- COGS 如何由毛利率倒推
- SG&A 如何区分固定费用和可变费用
- 利息费用和利息收入为什么要分开预测

---

## 2. 实务重点

在真实估值中，专业分析师通常不会简单假设现金流增长率，而是会：

```text
预测利润表
预测资产负债表
推导现金流量表
计算自由现金流
进行估值
```

这样得到的估值模型更有依据，也更容易向投资者或领导解释。

---

# 十四、一句话总结

财务报表建模的核心不是直接预测现金流，而是通过对未来利润表和资产负债表的逐项预测，构建出更加专业、可解释、可追溯的估值基础。
