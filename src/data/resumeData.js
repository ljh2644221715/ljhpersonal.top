export const resumeData = {
  personalInfo: {
    name: "李建华",
    title: "Artificial Intelligence Student & AI Agent Developer",
    location: "重庆",
    status: "人工智能专业本科在读",
    coreDirection: ["AI 智能体", "AI 应用开发", "智能系统开发"],
    summary:
      "科班出身，深度学习、智能算法的底子打得还算扎实。比起炫模型，我更喜欢拿 AI 解决实际问题——从搭工作流、写 Prompt、调 RAG 管线，到做 Web 全栈，都干过一遍。做过不少从零到一的项目，也踩过不少坑，回头看，最受益的还是那种「工程可落地」的思维方式。",
  },
  education: [
    {
      institution: "重庆对外经贸学院",
      degree: "工学学士",
      major: "人工智能",
      period: "2022.09 - 2026.06",
      coreCourses: [
        "机器学习",
        "图像处理",
        "自然语言处理",
        "深度学习",
        "人工智能",
      ],
      description:
        "课上做了 CNN、RNN 的实验，课下自己折腾 AI 应用落地和系统架构，两边都积累了不少经验。当了三年班长，带着班级拿过优秀班集体，平时也爱跑各种实践项目，入选美团校园俱乐部拿了优秀校园大使。",
      highlights: [
        {
          type: "position",
          title: "班长",
          description: "牵头策划大型班级活动，带领班级获优秀班集体荣誉",
        },
        {
          type: "club",
          title: "美团校园俱乐部 · 优秀校园大使",
          description: "深耕校园服务，获评优秀校园大使称号",
        },
        {
          type: "award",
          title: "优秀班集体",
          description: "统筹组织到位，团结班级齐心奋进",
        },
      ],
    },
  ],
  workExperience: [
    {
      company: "重庆智学力人工智能科技有限公司",
      position: "数据标注 / AI 训练师（实习）",
      period: "2026.01 - 2026.04",
      description:
        "第一次进到真实 AI 公司干活，接触了大量数据标注和模型训练的基础工作。这段经历让我对「数据决定模型上限」这话有了切身感受。",
      highlights: [
        "负责图像、文本、语音等多类型数据标注，熟练完成目标框选、语义分割、文本分类、语音转写等任务",
        "严格遵守标注规范，自查修正标注错误，保障数据精准度与合规性",
        "高效完成每日量化任务，按时提交成果，配合质检完成数据复核整改",
      ],
    },
  ],
  skills: {
    AI_Intelligence: [
      "Prompt Engineering",
      "LLM 工作流架构",
      "RAG 检索增强生成",
      "智能体（Agent）流程设计",
      "模型输出优化",
      "ComfyUI 工作流",
    ],
    FullStack_Development: [
      "Python",
      "Vue.js",
      "Flask",
      "API 深度集成",
      "WebSocket 实时通信",
      "JSON 数据流解析",
    ],
    System_Architecture: [
      "前后端分离架构设计",
      "高并发资源控制",
      "数据库事务控制",
      "RBAC 权限系统设计",
      "动态计费引擎建设",
    ],
    Tools_Platforms: [
      "ChatGPT / Gemini / Deepseek",
      "Office 办公套件",
      "Python 脚本与自动化",
      "ComfyUI / Stable Diffusion",
      "Git / Linux",
      "飞书 API / Webhook",
    ],
  },
  projects: [
    {
      name: "微信公众号智能客服 Agent",
      type: "AI 应用",
      techStack: ["腾讯元智", "RAG", "意图识别", "知识库"],
      period: "2026.04 - 至今",
      status: "ongoing",
      featured: true,
      description:
        "给准大一新生做了个迎新答疑的公众号智能体。把学校官方的物料和历史 Q&A 洗了一遍，搭了个业务知识库，用 RAG 外挂的方式让模型只回答校园强相关问题。折腾下来最满意的不是准确率，而是把「幻觉」压到了业务能接受的水平——官方答疑场景，严谨是第一位的。",
    },
    {
      name: "基于大模型的菜单图像生成 Agent",
      type: "AI 应用",
      techStack: ["Python", "ComfyUI", "LLM API", "Prompt Engineering"],
      period: "2026.02",
      status: "completed",
      featured: false,
      description:
        "做了个自动化出图流程：Python 调 LLM 写菜品提示词，扔给 ComfyUI 渲染，再自动命名归档。前期 JSON 解析和节点校验踩了不少坑，反复迭代 Prompt 才把稳定性和匹配度提上来。",
    },
    {
      name: "校园活动自动化聚合 Agent",
      type: "AI 应用",
      techStack: ["Python", "Charles", "逆向工程", "AI Skill"],
      period: "2025.12 - 至今",
      status: "ongoing",
      featured: true,
      description:
        "校园活动信息被锁在企业微信里，想看个完整活动列表都费劲。用 Charles 抓包把鉴权搞定了，写了 Python 脚本自动拉取清洗数据，再封装成 AI Skill，内置系统 Prompt 约束输出风格。原来要几个小时的采编工作，现在一键一分钟搞定。",
    },
    {
      name: "量化交易监控与智能预警系统",
      type: "全栈系统",
      techStack: ["Python", "定时任务", "飞书 Webhook", "容器化"],
      period: "2025.10 - 至今",
      status: "ongoing",
      featured: true,
      description:
        "不想天天盯着盘面看。搞了套定时任务调度流抓 A 股行情，量化分析模块把交易策略代码化，回测过滤出核心股票池，再搭高可用监控做高频盘口分析。深度接了飞书 Webhook，触发买卖点自动推富文本卡片到手机。容器化部署后跑了几个月，7x24 没宕过机。",
    },
    {
      name: "微信公众号私有化智能知识库",
      type: "AI 应用",
      techStack: ["Codex", "RAG", "向量化", "微信公众号"],
      period: "2025.08 - 至今",
      status: "ongoing",
      featured: false,
      description:
        "把公众号的海量历史文章做了向量化处理，搭了个私域知识图谱。接到后台后，粉丝提问能自动识别意图并拟人化回复，人工客服成本降了不少。",
    },
    {
      name: "校跑跑 - 校园生活服务平台",
      type: "创业项目",
      techStack: ["产品架构", "用户增长", "运营策略"],
      period: "2025.06 - 至今",
      status: "ongoing",
      featured: false,
      description:
        "从 0 开始搭了个校园服务平台，边做边摸索用户真正的痛点。到现在累计注册 3000+ 人，完成订单 5300+，交易额也破了万。虽说不算大，但每一步都是自己跑出来的。",
    },
    {
      name: "重庆对外经贸学院校园频道",
      type: "创业项目",
      techStack: ["内容运营", "用户增长", "社区管理"],
      period: "2024.11 - 至今",
      status: "ongoing",
      featured: false,
      description:
        "一年时间从 0 做到两万多用户。分析活跃时间段优化发布节奏后，单日浏览量稳定在 16 万以上。持续输出学生感兴趣的内容，维持了挺高的用户粘性。",
      link: "https://pd.qq.com/s/31p2np572?b=9",
    },
    {
      name: "交互式智能简历生成 Agent（Skill）",
      type: "AI 应用",
      techStack: ["Prompt Engineering", "Agent", "STAR 法则", "自动化"],
      period: "2025.07 - 2025.08",
      status: "completed",
      featured: false,
      description:
        "自己写简历时发现很多人（包括我）都掌握不好经历挖掘和亮点提炼。于是做了个引导式问答的智能体，Agent 化身虚拟面试官一步步引导用户深挖经历，底层 System Prompt 强制按 STAR 法则重构内容。输出格式化的标准简历文件，从对话到成稿全自动化。",
    },
    {
      name: "智慧停车管理系统（毕业设计）",
      type: "全栈系统",
      techStack: ["Python Flask", "Vue.js", "SocketIO", "事务控制"],
      period: "2025.03 - 2025.06",
      status: "completed",
      featured: false,
      description:
        "毕业设计做了个停车场管理系统。搞了基于距离和 VIP 等级的智能入场推荐，最麻烦的是高并发下防超卖——用「物理+虚拟容量」双层校验加数据库事务才搞定。配了阶梯计费和实时 Socket 引导，算是个完整的全栈活儿。",
    },
    {
      name: "AI 菜单图像生成智能体",
      type: "AI 应用",
      techStack: ["Python", "ComfyUI", "LLM API", "Prompt Engineering"],
      period: "2025.01 - 2025.02",
      status: "completed",
      featured: false,
      description:
        "构建了从文本到图像的自动化工作流，通过 Python 调度大语言模型生成结构化菜品提示词，结合 ComfyUI 文生图引擎渲染图像并完成命名标注。重点解决了 JSON 解析和节点校验的稳定性问题。",
    },
  ],
  practices_and_certifications: {
    algorithm: [
      "基于深度学习的图像去雾算法优化",
      "基于 CNN 的垃圾分类算法应用",
      "CNN 与 RNN 模型结构与训练全流程调优",
    ],
    certifications: [
      "科大讯飞 - 智能体工程师认证",
      "科大讯飞 - Prompt 工程师认证",
      "科大讯飞 - RAG 工程师认证",
      "科大讯飞 - 微调工程师认证",
    ],
    other_certifications: [
      "人工智能高级训练师",
    ],
  },
};
