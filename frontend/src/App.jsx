import React, { useState, useEffect } from 'react';
import { 
  Server, 
  Cpu, 
  Database, 
  CheckCircle2, 
  AlertCircle, 
  RefreshCw, 
  Layers, 
  ShieldCheck, 
  Activity, 
  Sparkles,
  ArrowRight,
  ExternalLink
} from 'lucide-react';
import { systemService } from './services/api';

export default function App() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastChecked, setLastChecked] = useState(null);

  const checkBackendHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await systemService.getHealth();
      setHealthData(data);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err) {
      setError(err.message || 'Failed to connect to backend server');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const projectModules = [
    { id: 1, name: "User Authentication", status: "Phase 2 Target", desc: "JWT, registration, user-isolated inventories" },
    { id: 2, name: "Smart Dashboard", status: "Upcoming", desc: "Real-time metrics, status cards, expiry radar" },
    { id: 3, name: "AI Item Recognition", status: "Upcoming", desc: "Universal image classification, OpenCV/YOLO, multi-item detection" },
    { id: 4, name: "Smart Inventory Core", status: "Upcoming", desc: "Category management, unit conversions, manual overrides" },
    { id: 5, name: "AI Consumption Prediction", status: "Upcoming", desc: "Usage rate computation, predictive depletion dates" },
    { id: 6, name: "Expiry & Storage Monitor", status: "Upcoming", desc: "Spoilage countdowns, temperature range guidelines" },
    { id: 7, name: "Intelligent Replenishment", status: "Upcoming", desc: "Manual, approval, and auto reorder triggers" },
    { id: 8, name: "Shopping Integration", status: "Upcoming", desc: "Simulated e-grocery matching, price comparisons" },
    { id: 9, name: "Automatic Payments", status: "Upcoming", desc: "Razorpay test mode, budget caps, digital receipts" },
    { id: 10, name: "Alerts & Notifications", status: "Upcoming", desc: "Low-stock, expiry, and payment status alerts" },
    { id: 11, name: "Analytics & Reports", status: "Upcoming", desc: "Consumption trends, spending breakdown, waste charts" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-cyan-500/20">
      {/* Top Navigation */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
                SmartFridge <span className="text-cyan-400">AI</span>
              </span>
              <span className="text-xs text-slate-400 block -mt-1 font-mono">
                Phase 1: Architecture & Scaffold
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={checkBackendHealth}
              disabled={loading}
              className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800/80 hover:bg-slate-800 text-xs font-medium text-slate-200 transition flex items-center gap-2"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin text-cyan-400' : ''}`} />
              Refresh Status
            </button>
            <a
              href="http://localhost:8000/api/v1/docs"
              target="_blank"
              rel="noreferrer"
              className="px-3 py-1.5 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-xs font-medium text-cyan-300 transition flex items-center gap-1.5"
            >
              <span>Swagger API Docs</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-b from-slate-900/90 to-slate-900/40 p-8">
          <div className="absolute top-0 right-0 -mt-8 -mr-8 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
          
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-800/50 text-cyan-300 text-xs font-medium">
              <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
              Phase 1 Successfully Initialized
            </div>
            
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Intelligent Refrigerator Monitoring & Replenishment
            </h1>
            
            <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
              Transforming traditional refrigeration into an autonomous household manager.
              Monitoring groceries, medicines, cosmetics, and prepared meals with universal AI object detection,
              predictive depletion modeling, and authorized automatic reordering.
            </p>
          </div>
        </div>

        {/* System Health Check Widget */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-cyan-400" />
              Live Backend Link & Health Check
            </h2>
            {lastChecked && (
              <span className="text-xs text-slate-500 font-mono">Last checked: {lastChecked}</span>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Status Card */}
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60">
              <div className="flex items-center justify-between">
                <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">Backend API</span>
                <Server className="h-4 w-4 text-slate-400" />
              </div>
              <div className="mt-3 flex items-center gap-2.5">
                {error ? (
                  <>
                    <AlertCircle className="h-5 w-5 text-rose-400" />
                    <div>
                      <div className="text-sm font-semibold text-rose-400">Disconnected</div>
                      <div className="text-xs text-slate-500">Run backend server on :8000</div>
                    </div>
                  </>
                ) : healthData ? (
                  <>
                    <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                    <div>
                      <div className="text-sm font-semibold text-emerald-400">Operational ({healthData.status})</div>
                      <div className="text-xs text-slate-400 font-mono">FastAPI v{healthData.version} (Python {healthData.python_version})</div>
                    </div>
                  </>
                ) : (
                  <div className="text-xs text-slate-400">Connecting to localhost:8000...</div>
                )}
              </div>
            </div>

            {/* Architecture Card */}
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60">
              <div className="flex items-center justify-between">
                <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">Hardware Layer</span>
                <Cpu className="h-4 w-4 text-slate-400" />
              </div>
              <div className="mt-3">
                <div className="text-sm font-semibold text-cyan-300">Software Simulation Mode</div>
                <div className="text-xs text-slate-400 mt-1">
                  Ready for camera hooks, door triggers, and weight sensors
                </div>
              </div>
            </div>

            {/* Database Card */}
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60">
              <div className="flex items-center justify-between">
                <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">Database Engine</span>
                <Database className="h-4 w-4 text-slate-400" />
              </div>
              <div className="mt-3">
                <div className="text-sm font-semibold text-slate-200">PostgreSQL + SQLAlchemy</div>
                <div className="text-xs text-slate-400 mt-1">
                  Normalized schema & user multi-tenancy ready
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Project Architecture Overview */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Layers className="h-5 w-5 text-cyan-400" />
            System Architecture & Data Flow
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-2">
              <div className="text-xs font-mono text-cyan-400 font-semibold">LAYER 1: PRESENTATION</div>
              <div className="font-semibold text-white text-sm">Vite + React 19 + Tailwind</div>
              <p className="text-xs text-slate-400">
                Responsive dashboard, camera/photo upload dropzones, Recharts consumption metrics, and cart management.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-2">
              <div className="text-xs font-mono text-cyan-400 font-semibold">LAYER 2: APPLICATION API</div>
              <div className="font-semibold text-white text-sm">FastAPI REST Framework</div>
              <p className="text-xs text-slate-400">
                JWT Auth, tenant isolation, asynchronous image processing pipelines, and background job coordination.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-2">
              <div className="text-xs font-mono text-cyan-400 font-semibold">LAYER 3: INTELLIGENCE</div>
              <div className="font-semibold text-white text-sm">OpenCV + YOLO + ML Regressors</div>
              <p className="text-xs text-slate-400">
                Universal classification (groceries, medicines, skincare, meals), moving-average depletion forecasts.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-2">
              <div className="text-xs font-mono text-cyan-400 font-semibold">LAYER 4: PERSISTENCE</div>
              <div className="font-semibold text-white text-sm">PostgreSQL + Static Storage</div>
              <p className="text-xs text-slate-400">
                ACID relational tables, audit logs, consumption series, and secure uploaded image storage.
              </p>
            </div>
          </div>
        </section>

        {/* Roadmap Grid */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-cyan-400" />
            Module Delivery Roadmap (Phase 2 to 11)
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {projectModules.map((m) => (
              <div 
                key={m.id} 
                className="p-4 rounded-xl border border-slate-800/70 bg-slate-900/30 hover:border-slate-700/80 transition"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-slate-500 font-semibold">MODULE {String(m.id).padStart(2, '0')}</span>
                  <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${
                    m.id === 1 ? 'bg-cyan-950 text-cyan-300 border border-cyan-800' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {m.status}
                  </span>
                </div>
                <div className="text-sm font-semibold text-slate-200">{m.name}</div>
                <div className="text-xs text-slate-400 mt-1">{m.desc}</div>
              </div>
            ))}
          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 mt-12 py-6 text-center text-xs text-slate-500">
        SmartFridge AI • Initialized under Phase 1 Architecture • Ready for Phase 2 Implementation
      </footer>
    </div>
  );
}
