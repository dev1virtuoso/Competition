#set page(
  paper: "presentation-16-9",
  margin: 1.8cm,
  fill: rgb("#ffffff"),
  footer: context [
    #set text(size: 11pt, fill: gray)
    #line(length: 100%, stroke: 0.5pt + gray)
    #grid(
      columns: (1fr, 1fr),
      [虾壳式关节仿生设计],
      align(right)[第 #counter(page).display() / 27 页]
    )
  ]
)

#set text(
  font: ("Times New Roman"),
  size: 16pt,
  lang: "zh"
)
#set par(justify: true, leading: 1.15em)

#let my-slide(title: "", body) = {
  pagebreak(weak: true)
  v(-0.8cm)
  block(
    width: 100%,
    inset: (bottom: 0.6em),
    stroke: (bottom: 3pt + rgb("#0055cc"))
  )[
    #text(26pt, weight: "bold", fill: rgb("#0055cc"))[#title]
  ]
  v(1.2em)
  body
}

#align(center + horizon)[
  #text(36pt, weight: "bold", fill: rgb("#003399"))[仿生虾壳式机械人关节设计]
  
  #v(1em)
  #text(20pt, fill: gray)[自然刚柔耦合 · 低成本高灵活人形机械人关节核心技术]
  
  #v(4em)
  #grid(
    columns: (auto, auto),
    column-gutter: 1em,
    row-gutter: 0.8em,
    align: left,
    text(16pt)[项目团队：], text(16pt)[機腱科技（Robotech HK）],
    text(16pt)[日期：],   text(16pt)[2026年4月12日]
  )
]

#my-slide(title: "项目名称与简介")[
  *项目名称*：機腱科技（Robotech HK）仿生虾壳式机械人关节设计

  *项目简介*：
  本项目旨在开发一款新颖的机械人关节设计，采用仿生设计，通过模仿虾壳的结构和功能，提升机械或人工智能系统的机动性能。

  *核心特点*：
  - 自然灵巧，刚柔耦合
  - 低成本、高强度、易伸展的机械人核心技术

  *具体设计思路与分析*：
  - 刚柔一体化：通过结合刚性和柔性材料，模仿虾壳的结构特性，使关节既能承受较大的机械负载，又能灵活运动。
  - 反向共轭面设计（Reverse Conjugate Surface）：这种设计能够优化关节的运动范围和传动效率，同时减少机械结构的复杂性。

]

#my-slide(title: "1. 理念由来（切入点）")[
  传统人形机械人关节普遍采用以下方案：

  #set text(size: 18pt)
  #set par(leading: 0.75em)
  #table(
    columns: (1.8fr, 1fr, 2.5fr),
    stroke: 0.5pt + gray,
    fill: (x, y) => if y == 0 { rgb("#f0f7ff") },
    [*关节类型*], [*成本占比*], [*主要缺点*],
    [传统刚性多轴关节（齿轮/减速器）], [60%–70%], [灵活性差、重量大、无法实现大角度极端姿态],
    [谐波减速器关节], [45%–55%], [成本极高、结构复杂、维护困难、能耗高],
    [纯拮抗腱驱动关节], [55%–65%], [电机数量多、同步控制难、长期磨损严重],
  )
  #set par(leading: 1.15em)
  #set text(size: 15pt)

  这些方案共同痛点：高成本与灵活性不足。

  我们从虾类腹部外骨骼的「多段刚性壳及柔性连接」天然结构中获得灵感，提出虾壳式多段混合关节，旨在以更低成本实现更高的运动灵活性。
]

#my-slide(title: "传统关节类型与应用场景对比")[
  #text(19pt, weight: "bold")[传统主流关节类型及其典型应用场景]

  #v(1em)
  #set text(size: 15pt)
  #table(
    columns: (1.4fr, 2fr, 2.8fr),
    stroke: 0.5pt + gray,
    inset: 9pt,
    fill: (x, y) => if y == 0 { rgb("#f0f7ff") },
    table.header(
      [*关节类型*], 
      [*结构特点*], 
      [*典型应用场景*]
    ),
    [
      #image("traditional_rigid_joint.png", width: 60%)
      传统刚性多轴关节\
      （齿轮/减速器）
    ],
    [结构简单、刚性强、精度较高],
    [工业自动化、精密装配线、CNC机床、焊接机械人、通用工业机械臂 #image("cnc_machine.jpg", width: 35%)]
    ,
    [
      #image("harmonic_drive_joint.jpg", width: 60%)
      谐波减速器关节
    ],
    [体积小、减速比大、精度极高、扭矩大],
    [汽车制造（焊接、喷涂、装配）、医疗手术机械人、航天航空高端装备、高精度工业机械人 #image("surgical_robots.jpg", width: 35%)]
    ,
    [
      #image("antagonistic_tendon_joint.jpg", width: 60%)
      纯拮抗腱驱动关节
    ],
    [重量轻、柔顺性较好、电机数量多],
    [轻型协作机械人、物流仓储（AGV小车）、部分服务型机械人、需要一定柔顺性的场景 #image("agv.png", width: 35%)]
  )

  #v(1em)
  #text(17pt, weight: "bold", fill: rgb("#cc0000"))[共同局限：成本高昂且灵活性不足，难以实现大范围极端姿态]
]

#my-slide(title: "2. 市场的需要（市场前景）")[
  人形机械人市场正高速增长：

  - 2025 年全球市场规模约 29 亿美元
  - 预计 2030 年达 152 亿美元（CAGR 39.2%）

  核心需求：高灵活腰部/脊柱、支持极端姿态（舞蹈、后仰、劈叉），同时兼顾低成本量产。
]

#my-slide(title: "3. 我们的方案")[
  虾壳式多段柔性关节模块

  - 5 段仿生脊柱/腰部结构
  - 支持 90°+ 后仰桥、180°+ 劈叉、单腿过头抬高
  - 结合腱驱动、弹簧回位与欠驱动优化
  - 目标成本 < 770 美金（V6 版本）

  核心价值：以可接受的成本实现接近生物水平的灵活性与顺应性。
]

#my-slide(title: "4. 市场分析")[
  当前主要竞争方案：

  - Boston Dynamics Atlas：性能领先，但成本极高
  - Figure / Tesla Optimus：通用性强，腰部灵活性相对保守
  - Unitree / Agility Robotics：性价比高，但极端姿态能力不足

  主流方案仍以传统刚性关节或高成本精密关节为主。
]

#my-slide(title: "5. 设计对比（我们的优势）")[
  #set text(size: 16pt)
  #set par(leading: 0.7em)
  #table(
    columns: (1.4fr, 2fr, 2.5fr),
    stroke: 0.5pt + gray,
    fill: (x, y) => if y == 0 { rgb("#f0f7ff") },
    [*对比维度*], [*现有主流设计*], [*我们的虾壳式设计*],
    [运动范围], [受限于单轴刚性，极端姿态困难], [多段设计，支持 90°+ 后仰、180°+ 劈叉],
    [成本], [60%–70% 机械人总成本], [欠驱动优化，显著降低成本],
    [灵活性/顺应性], [刚性强、冲击吸收差], [刚柔耦合，良好冲击吸收],
    [复杂度/电机数量], [较高], [显著减少（弹簧回位及共享电机）],
    [控制难度], [同步困难、能耗较高], [PPO 强化学习及微操作分解，较为平滑],
  )
  #set par(leading: 1.15em)
  #set text(size: 15pt)

  #v(0.8em)
  #text(19pt, weight: "bold")[结论：相较于现有主流关节设计，我们的虾壳式关节在运动灵活性、系统成本控制以及结构可靠性上具备显著竞争优势。]
]

#my-slide(title: "6. 我们的虾壳式关节设计：CAD 展示")[
  #align(center)[
    #text(18pt, weight: "bold")[虾壳式多段关节完整 CAD 模型]

    #v(1.5em)
    #image("971.PNG", width: 20%)

    #v(0.8em)
    #text(15pt, fill: gray)[4 段刚性壳，Dyneema 腱缆路由及弹簧回位机构]
  ]
]

#my-slide(title: "6. 我们的虾壳式关节设计：CAD 展示")[
  #align(center)[
    #text(18pt, weight: "bold")[虾壳式多段关节完整 CAD 模型]

    #v(1.5em)
    #image("971.PNG", width: 20%)

    #v(0.8em)
    #text(15pt, fill: gray)[前视图]
  ]
]

#my-slide(title: "6. 我们的虾壳式关节设计：CAD 展示")[
  #align(center)[
    #text(18pt, weight: "bold")[虾壳式多段关节完整 CAD 模型]

    #v(1.5em)
    #image("957.JPG", width: 40%)

    #v(0.8em)
    #text(15pt, fill: gray)[侧视图]
  ]
]

#my-slide(title: "6. 我们的虾壳式关节设计：CAD 展示")[
  #align(center)[
    #text(18pt, weight: "bold")[虾壳式多段关节完整 CAD 模型]

    #v(1.5em)
    #image("958.JPG", width: 40%)

    #v(0.8em)
    #text(15pt, fill: gray)[俯视图]
  ]
]

#my-slide(title: "6. 我们的虾壳式关节设计：CAD 展示")[
  #align(center)[
    #text(18pt, weight: "bold")[虾壳式多段关节完整 CAD 模型]

    #v(1.5em)
    #image("IMG_0551.jpg", width: 20%)

    #v(0.8em)
    #text(15pt, fill: gray)[爆炸图]
  ]
]

#my-slide(title: "6. 我们的虾壳式关节设计：CAD 展示")[
  #align(center)[
    #text(18pt, weight: "bold")[虾壳式多段关节完整 CAD 模型]

    #v(1.5em)
    #image("cad_shrimp_shell_joint.jpg", width: 40%)

    #v(0.8em)
    #text(15pt, fill: gray)[影片]
  ]
]

#my-slide(title: "7. 研发路径")[
  研发路径与积累：

  - 2016–2025 年：V1 至 V5 多个版本持续迭代
  - 核心技术：Dyneema 高强度腱缆、精密滑轮路由、PPO 强化学习及微操作分解
  - 仿真验证：MuJoCo 平台多次完成关键物理动作验证
  - 2026 年计划：完成 V6 低成本实物原型并进行进一步灵巧化扩展
]

#my-slide(title: "8. 市场运作策略")[
  我们将采取以下策略将技术优势转化为市场价值：

  - 模块化销售及开放源代码，快速获取早期用户
  - 与人形机械人整机厂商进行深度集成合作
  - 针对康复医疗、教育及娱乐领域推出定制解决方案
  - 通过演示视频、开源社区及行业展会建立品牌认知
]

#my-slide(title: "9. 盈利模式")[
  多层次可持续盈利模式：

  - 核心硬件模块销售（关节组件与腰部系统）
  - 技术授权与知识产权许可
  - 定制开发与系统集成服务
  - 未来开源社区增值服务及应用订阅

  预计随人形机械人市场爆发，3–5 年内可实现规模化盈利。
]

#my-slide(title: "10. 风险与应对措施")[
  #set text(size: 16pt)
  #table(
    columns: (1.4fr, 2fr, 2.5fr),
    stroke: 0.5pt + gray,
    fill: (x, y) => if y == 0 { rgb("#f0f7ff") },
    table.header([*风险名称*], [*风险描述*], [*解决方案*]),
    [技术风险], [腱缆长期磨损、弹簧回程间隙], [选用高强度低摩擦 Dyneema 纤维，进行加速寿命测试，并开发自适应张力补偿算法],
    [制造成本风险], [量产时成本超出预期], [采用欠驱动设计减少电机数量，优化供应链并批量采购],
    [市场接受风险], [整机厂商对新方案接受度低], [提供开源代码与 MuJoCo 仿真模型，推出小批量验证套件逐步建立案例],
    [供应链风险], [关键材料供应不稳定], [开发替代材料方案，并与多家供应商建立战略合作]
  )
  #set text(size: 15pt)
]

#my-slide(title: "11. 核心团队优势")[
  #set text(size: 15pt)
  #table(
    columns: (1.4fr, 2fr, 2.5fr),
    stroke: 0.5pt + gray,
    fill: (x, y) => if y == 0 { rgb("#f0f7ff") },
    table.header([*成员*], [*角色*], [*描述*]),
    [#image("patrick_lee.jpg", width: 35%) Patrick Lee], [项目管理], [拥有30年海外及国内IT/AI项目管理经验],
    [Sam Lau], [系统开发], [年轻且富有创意的开源IT/AI系统开发者],
    [Carson Wu], [技术设计], [自12岁起开始钻研机械人设计，专注低成本人形机械人研发与迭代]
  )
  #set text(size: 15pt)
]

#my-slide(title: "本设计应用场景")[
  虾壳式关节具有高灵活性、低成本和大范围运动能力，可广泛应用于：

  - *人形机械人*：舞蹈表演、娱乐互动、服务机械人
  - *康复医疗*：外骨骼康复设备、辅助行走系统
  - *工业制造*：柔性装配臂、协作机械人
  - *教育与研究*：开源机械人平台、STEM教育套件
  - *特种领域*：救援机械人
]

#my-slide(title: "市场运作策略")[
  我们将采取以下策略将技术优势转化为市场价值：

  - 模块化销售及开放源代码，快速获取早期用户
  - 与人形机械人整机厂商进行深度集成合作
  - 针对康复医疗、教育及娱乐领域推出定制解决方案
  - 通过演示视频、开源社区及行业展会建立品牌认知
]

#my-slide(title: "盈利模式")[
  多层次可持续盈利模式：

  - 核心硬件模块销售（关节组件与腰部系统）
  - 技术授权与知识产权许可
  - 定制开发与系统集成服务
  - 未来开源社区增值服务及应用订阅

  预计随人形机械人市场爆发，3–5 年内可实现规模化盈利。
]

#my-slide(title: "12. 项目需求")[
  *项目需求*：

  - *集资*：寻求战略投资或众筹，支持V6实物原型开发与小批量生产
  - *对接大学研究团队*：与香港及内地高校机械人实验室合作，进行联合研发与技术验证
  - *专利申请*：尽快申请核心技术专利（虾壳式多段关节结构、反向共轭面设计、欠驱动控制方法等），保护知识产权

  欢迎有意向的机构或投资人共同推进项目落地。
]

#my-slide(title: "感谢聆听")[
  #align(center + horizon)[
    #text(25pt, weight: "bold", fill: rgb("#003399"))[仿生虾壳式关节设计]

    #v(2em)
    通过仿生虾壳式机械人关节设计，我们致力于推动人形机械人技术平民化，让灵活、智能且高性价比的机械人系统走进每一家企业与学校，真正实现降本增效与智能化转型。

    #v(3em)
    #text(20pt)[欢迎交流与合作]
  ]
]