import type {
  Client,
  LiteracyModule,
  Quiz,
  ReadinessBreakdown,
} from "../types";

const delay = <T>(value: T, ms = 350): Promise<T> =>
  new Promise((resolve) => setTimeout(() => resolve(value), ms));

const COOPS = ["Dakar Central", "Ashanti Textiles", "Nairobi Market", "Kampala Growers", "Lagos Traders"];
const FIRST = ["Amara", "Kofi", "Adama", "Kwame", "Fatou", "Chinedu", "Zara", "Nia", "Tunde", "Aisha", "Jabari", "Lerato"];
const LAST = ["Okafor", "Mensah", "Diop", "Adebayo", "Owusu", "Achebe", "Nakato", "Sankara", "Mwangi", "Banda"];

function rand<T>(arr: T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }

function makeClient(i: number): Client {
  const progress = Math.min(100, Math.max(5, Math.round(20 + Math.random() * 80)));
  const score = Math.min(100, Math.max(20, Math.round(progress * 0.7 + Math.random() * 30)));
  const cat =
    score >= 80 ? "Strong" : score >= 65 ? "Ready" : score >= 45 ? "Developing" : "Building";
  return {
    id: `c_${i}`,
    name: `${rand(FIRST)} ${rand(LAST)}`,
    phone: `+254 7${Math.floor(10000000 + Math.random() * 89999999)}`,
    cooperative: rand(COOPS),
    joinedAt: new Date(Date.now() - Math.random() * 1000 * 60 * 60 * 24 * 365).toISOString(),
    literacyProgress: progress,
    readinessScore: score,
    category: cat,
    lastActive: ["2h ago", "5h ago", "Yesterday", "3 days ago", "1 week ago"][i % 5],
  };
}

const CLIENTS: Client[] = Array.from({ length: 42 }, (_, i) => makeClient(i));

const MODULES: LiteracyModule[] = [
  {
    id: "m1",
    title: "Basics of Savings",
    description: "Why saving matters and simple habits to build it.",
    durationMin: 15,
    category: "Foundations",
    progress: 100,
    lessons: [
      { id: "l1", title: "What is saving?", body: "Saving is setting aside money today for needs tomorrow. Even small amounts add up over time. Start with what you can - consistency matters more than size.", completed: true },
      { id: "l2", title: "Setting a savings goal", body: "A clear goal - a new sewing machine, a school fee - turns saving into a plan. Write it down and pick a date.", completed: true },
      { id: "l3", title: "Daily vs weekly saving", body: "Choose a rhythm that matches your income. Daily for traders, weekly for salaried, monthly for cooperative members.", completed: true },
    ],
  },
  {
    id: "m2",
    title: "Understanding Interest",
    description: "How borrowing costs work and how to read a rate.",
    durationMin: 20,
    category: "Credit",
    progress: 60,
    lessons: [
      { id: "l1", title: "What is interest?", body: "Interest is the price you pay to borrow money - or earn when you save. It is usually stated as a percentage per year (APR).", completed: true },
      { id: "l2", title: "Reading a loan offer", body: "Compare the total amount you repay, not just the monthly figure. A small monthly payment over a long period can cost more.", completed: true },
      { id: "l3", title: "Avoiding predatory rates", body: "If the cost of borrowing is more than what your business earns, the loan will trap you. Ask for the APR and compare two lenders.", completed: false },
    ],
  },
  {
    id: "m3",
    title: "Cash Flow for Small Business",
    description: "Knowing what comes in and what goes out, weekly.",
    durationMin: 25,
    category: "Business",
    progress: 30,
    lessons: [
      { id: "l1", title: "Money in, money out", body: "Cash flow is the difference between what you receive and what you spend. Positive cash flow means your business can pay its bills.", completed: true },
      { id: "l2", title: "A simple weekly ledger", body: "On Sunday evening, list sales and expenses for the week. The gap is your profit - or your warning sign.", completed: false },
      { id: "l3", title: "Saving for slow weeks", body: "Set aside a portion of strong weeks for slow ones. A cushion of two weeks of expenses is a good first goal.", completed: false },
    ],
  },
  {
    id: "m4",
    title: "Building an Emergency Buffer",
    description: "Preparing for the unexpected without going into debt.",
    durationMin: 18,
    category: "Foundations",
    progress: 0,
    lessons: [
      { id: "l1", title: "Why a buffer matters", body: "Emergencies will come. A buffer lets you handle them without borrowing at high cost.", completed: false },
      { id: "l2", title: "How much is enough?", body: "Start with one week of essential expenses. Build to one month over a year.", completed: false },
    ],
  },
];

const QUIZZES: Quiz[] = [
  {
    id: "q1",
    moduleId: "m2",
    title: "Understanding Interest - Check Your Knowledge",
    questions: [
      {
        id: "qq1",
        prompt: "If your business earns $200 in a week and you spent $180 on materials, what is your net profit?",
        options: ["$380", "$20", "$180", "$200"],
        correctIndex: 1,
        explanation: "Net profit is income minus expenses: $200 − $180 = $20.",
      },
      {
        id: "qq2",
        prompt: "Which loan is more expensive overall?",
        options: ["$100 at 5% per month for 6 months", "$100 at 30% per year for 6 months"],
        correctIndex: 0,
        explanation: "5% per month is roughly 60% per year - much higher than 30% per year.",
      },
      {
        id: "qq3",
        prompt: "What does APR stand for?",
        options: ["Annual Payment Rate", "Annual Percentage Rate", "Average Profit Return", "Account Performance Ratio"],
        correctIndex: 1,
        explanation: "APR - Annual Percentage Rate - is the yearly cost of borrowing as a percentage.",
      },
    ],
  },
];

const READINESS: ReadinessBreakdown = {
  score: 78,
  category: "Ready",
  factors: [
    { label: "Consistent savings habits", status: "active", detail: "12 weeks of regular deposits" },
    { label: "Literacy modules complete", status: "partial", detail: "2 of 4 modules finished" },
    { label: "Cooperative participation", status: "active", detail: "Active member, Dakar Central" },
    { label: "Income verification", status: "pending", detail: "Submit last 3 months of records" },
  ],
  suggestions: [
    "Finish the Cash Flow module to add 8 points to your score.",
    "Submit income records to unlock larger loan limits.",
    "Maintain weekly savings for 4 more weeks to reach Strong category.",
  ],
};

export const mock = {
  clients: () => delay(CLIENTS),
  client: (id: string) => delay(CLIENTS.find((c) => c.id === id) ?? null),
  modules: () => delay(MODULES),
  module: (id: string) => delay(MODULES.find((m) => m.id === id) ?? null),
  quiz: (id: string) => delay(QUIZZES.find((q) => q.id === id) ?? null),
  quizByModule: (moduleId: string) => delay(QUIZZES.find((q) => q.moduleId === moduleId) ?? null),
  readiness: () => delay(READINESS),
  dashboard: () =>
    delay({
      totalClients: CLIENTS.length,
      activeLearners: CLIENTS.filter((c) => c.literacyProgress > 10 && c.literacyProgress < 100).length,
      averageReadiness: Math.round(CLIENTS.reduce((a, c) => a + c.readinessScore, 0) / CLIENTS.length),
      completionRate: Math.round(CLIENTS.filter((c) => c.literacyProgress === 100).length / CLIENTS.length * 100),
      trend: Array.from({ length: 8 }, (_, i) => ({
        week: `W${i + 1}`,
        completion: 30 + Math.round(Math.random() * 50 + i * 4),
        readiness: 50 + Math.round(Math.random() * 20 + i * 2),
      })),
      distribution: [
        { name: "Building", value: CLIENTS.filter((c) => c.category === "Building").length },
        { name: "Developing", value: CLIENTS.filter((c) => c.category === "Developing").length },
        { name: "Ready", value: CLIENTS.filter((c) => c.category === "Ready").length },
        { name: "Strong", value: CLIENTS.filter((c) => c.category === "Strong").length },
      ],
      modulePerf: MODULES.map((m) => ({
        name: m.title.split(" ").slice(0, 2).join(" "),
        completion: 30 + Math.round(Math.random() * 60),
      })),
    }),
};
