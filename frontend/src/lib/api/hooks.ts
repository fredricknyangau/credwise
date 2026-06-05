import { useQuery } from "@tanstack/react-query";
import { mock } from "./mock";
import { api, USE_MOCKS } from "./client";

export const qk = {
  dashboard: ["mfi", "dashboard"] as const,
  clients: ["mfi", "clients"] as const,
  client: (id: string) => ["mfi", "client", id] as const,
  modules: ["portal", "modules"] as const,
  module: (id: string) => ["portal", "module", id] as const,
  quiz: (id: string) => ["portal", "quiz", id] as const,
  quizByModule: (id: string) => ["portal", "quiz-by-module", id] as const,
  readiness: ["portal", "readiness"] as const,
};

export const useDashboard = () =>
  useQuery({
    queryKey: qk.dashboard,
    queryFn: async () => {
      if (USE_MOCKS) return mock.dashboard();
      
      const res = await api.get("/analytics/dashboard");
      const data = res.data.data;
      
      const [trendRes, moduleRes] = await Promise.all([
        api.get("/analytics/literacy-trend"),
        api.get("/analytics/module-completion"),
      ]);

      return {
        totalClients: data.total_clients,
        activeLearners: data.active_clients,
        averageReadiness: Math.round(data.avg_readiness_score),
        completionRate: Math.round(data.avg_literacy_completion),
        trend: trendRes.data.data.map((t: any, idx: number) => ({
          week: `W${idx + 1}`,
          completion: t.completions,
          readiness: Math.round(data.avg_readiness_score),
        })),
        distribution: [
          { name: "Building", value: Math.round(data.total_clients * 0.2) },
          { name: "Developing", value: Math.round(data.total_clients * 0.3) },
          { name: "Ready", value: Math.round(data.total_clients * 0.4) },
          { name: "Strong", value: Math.round(data.total_clients * 0.1) },
        ],
        modulePerf: moduleRes.data.data.map((m: any) => ({
          name: m.title.split(" ").slice(0, 2).join(" "),
          completion: Math.round(m.completion_rate),
        })),
      };
    },
  });

export const useClients = () =>
  useQuery({
    queryKey: qk.clients,
    queryFn: async () => {
      if (USE_MOCKS) return mock.clients();
      const res = await api.get("/users/");
      const items = res.data.data.items || [];
      return items.map((c: any) => ({
        id: c.id,
        name: c.full_name,
        phone: c.phone_number,
        cooperative: c.cooperative_member ? "Active Coop Member" : "None",
        joinedAt: c.created_at,
        literacyProgress: Math.round(c.literacy_progress),
        readinessScore: Math.round(c.readiness_score),
        category: c.category,
        lastActive: c.is_active ? "Active" : "Suspended",
      }));
    },
  });

export const useClient = (id: string) =>
  useQuery({
    queryKey: qk.client(id),
    queryFn: async () => {
      if (USE_MOCKS) return mock.client(id);
      const res = await api.get(`/users/${id}`);
      const c = res.data.data;
      return {
        id: c.id,
        name: c.full_name,
        phone: c.phone_number,
        cooperative: c.cooperative_member ? "Active Coop Member" : "None",
        joinedAt: c.created_at,
        literacyProgress: Math.round(c.literacy_progress),
        readinessScore: Math.round(c.readiness_score),
        category: c.category,
        lastActive: c.is_active ? "Active" : "Suspended",
      };
    },
    enabled: !!id,
  });

export const useModules = () =>
  useQuery({
    queryKey: qk.modules,
    queryFn: async () => {
      if (USE_MOCKS) return mock.modules();
      const res = await api.get("/literacy/modules");
      return res.data.data.map((m: any) => ({
        id: m.id,
        title: m.title,
        description: m.description,
        durationMin: m.estimated_minutes,
        category: m.difficulty_level,
        progress: Math.round(m.progress_percentage || 0),
        lessons: (m.lessons || []).map((l: any) => ({
          id: l.id,
          title: l.title,
          body: l.content,
          completed: l.is_completed,
        })),
      }));
    },
  });

export const useModule = (id: string) =>
  useQuery({
    queryKey: qk.module(id),
    queryFn: async () => {
      if (USE_MOCKS) return mock.module(id);
      const res = await api.get(`/literacy/modules/${id}`);
      const m = res.data.data;
      return {
        id: m.id,
        title: m.title,
        description: m.description,
        durationMin: m.estimated_minutes,
        category: m.difficulty_level,
        progress: Math.round(m.progress_percentage || 0),
        lessons: (m.lessons || []).map((l: any) => ({
          id: l.id,
          title: l.title,
          body: l.content,
          completed: l.is_completed,
        })),
      };
    },
    enabled: !!id,
  });

export const useQuiz = (id: string) =>
  useQuery({
    queryKey: qk.quiz(id),
    queryFn: async () => {
      if (USE_MOCKS) return mock.quiz(id);
      const res = await api.get(`/quizzes/${id}`);
      const q = res.data.data;
      return {
        id: q.id,
        moduleId: q.module_id,
        title: q.title,
        questions: (q.questions || []).map((qn: any) => ({
          id: qn.id,
          prompt: qn.question,
          options: qn.options,
          correctIndex: qn.options.indexOf(qn.correct_answer),
          explanation: "Check the course material for more information.",
        })),
      };
    },
    enabled: !!id,
  });

export const useQuizByModule = (moduleId: string) =>
  useQuery({
    queryKey: qk.quizByModule(moduleId),
    queryFn: async () => {
      if (USE_MOCKS) return mock.quizByModule(moduleId);
      const res = await api.get(`/quizzes/modules/${moduleId}`);
      const q = res.data.data;
      return {
        id: q.id,
        moduleId: q.module_id,
        title: q.title,
        questions: (q.questions || []).map((qn: any) => ({
          id: qn.id,
          prompt: qn.question,
          options: qn.options,
          correctIndex: qn.options.indexOf(qn.correct_answer),
          explanation: "Check the course material for more information.",
        })),
      };
    },
    enabled: !!moduleId,
  });

export const useReadiness = () =>
  useQuery({
    queryKey: qk.readiness,
    queryFn: async () => {
      if (USE_MOCKS) return mock.readiness();
      const res = await api.get("/credit-scores/me");
      const d = res.data.data;
      if (!d) return null;
      return {
        score: Math.round(d.score),
        category: d.rating,
        factors: (d.factors || []).map((f: string) => ({
          label: f,
          status: "active",
          detail: "",
        })),
        suggestions: [
          "Continue completing your education modules to boost your score.",
          "Maintain regular saving habits.",
        ],
      };
    },
  });
