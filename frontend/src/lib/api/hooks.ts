import { useQuery } from "@tanstack/react-query";
import { mock } from "./mock";
// import { api, USE_MOCKS } from "./client";  // wire to FastAPI when available

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

export const useDashboard = () => useQuery({ queryKey: qk.dashboard, queryFn: mock.dashboard });
export const useClients = () => useQuery({ queryKey: qk.clients, queryFn: mock.clients });
export const useClient = (id: string) =>
  useQuery({ queryKey: qk.client(id), queryFn: () => mock.client(id), enabled: !!id });
export const useModules = () => useQuery({ queryKey: qk.modules, queryFn: mock.modules });
export const useModule = (id: string) =>
  useQuery({ queryKey: qk.module(id), queryFn: () => mock.module(id), enabled: !!id });
export const useQuiz = (id: string) =>
  useQuery({ queryKey: qk.quiz(id), queryFn: () => mock.quiz(id), enabled: !!id });
export const useQuizByModule = (moduleId: string) =>
  useQuery({ queryKey: qk.quizByModule(moduleId), queryFn: () => mock.quizByModule(moduleId), enabled: !!moduleId });
export const useReadiness = () => useQuery({ queryKey: qk.readiness, queryFn: mock.readiness });
