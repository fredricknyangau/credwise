export type UserRole = "mfi_admin" | "client";

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  organization?: string;
}

export interface Client {
  id: string;
  name: string;
  phone: string;
  cooperative: string;
  joinedAt: string;
  literacyProgress: number; // 0-100
  readinessScore: number; // 0-100
  category: ReadinessCategory;
  lastActive: string;
}

export type ReadinessCategory = "Building" | "Developing" | "Ready" | "Strong";

export interface LiteracyModule {
  id: string;
  title: string;
  description: string;
  durationMin: number;
  lessons: Lesson[];
  progress: number; // 0-100
  category: string;
}

export interface Lesson {
  id: string;
  title: string;
  body: string;
  completed: boolean;
}

export interface QuizQuestion {
  id: string;
  prompt: string;
  options: string[];
  correctIndex: number;
  explanation: string;
}

export interface Quiz {
  id: string;
  moduleId: string;
  title: string;
  questions: QuizQuestion[];
}

export interface FinancialProfile {
  incomeRange: string;
  savingsHabit: string;
  businessType: string;
  cooperative: string;
  monthsInBusiness: number;
}

export interface ReadinessBreakdown {
  score: number;
  category: ReadinessCategory;
  factors: { label: string; status: "active" | "partial" | "pending"; detail: string }[];
  suggestions: string[];
}
