import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  Camera, 
  TrendingDown, 
  RefreshCw, 
  Clock, 
  CreditCard,
  Server,
  Activity,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { systemService } from '../services/api';

export default function Landing() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    systemService.getHealth()
      .then(setHealthData)
      .catch((err) => setError(err.message || "Failed to reach backend"))
      .finally(() => setLoading(false));
  }, []);

  const features = [
    {
      icon: Camera,
      title: "Universal Object Detection",
      desc: "Upload photos of fridge shelves to detect groceries, medicines, cosmetics, and leftovers automatically."
    },
    {
      icon: TrendingDown,
      title: "AI Depletion Forecasting",
      desc: "Learns household consumption rates to predict the exact day items will run out before you notice."
    },
    {
      icon: Clock,
      title: "Active Expiry Radar",
      desc: "Color-coded countdowns and storage temperature warnings prevent food and medicine spoilage."
    },
    {
      icon: RefreshCw,
      title: "Autonomous Replenishment",
      desc: "Smart cart creation with Manual, Approval, or Fully Automatic purchasing modes."
    },
    {
      icon: CreditCard,
      title: "Simulated Automated Pay",
      desc: "Razorpay test mode with monthly spending caps and transaction receipt generation."
    },
    {
      icon: ShieldCheck,
      title: "Isolated Multi-Tenancy",
      desc: "JWT-secured architecture keeping your family's refrigerator contents strictly confidential."
    }
  ];

  return (
    <div className="space-y-16 py-8">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900/90 via-slate-900/50 to-slate-950 p-8 sm:p-12">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800 text-cyan-300 text-xs font-semibold">
            <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
            Smart Refrigerator Management Powered by AI
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Never Run Out. Never Waste Food. <br />
            <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              Your Autonomous Kitchen Assistant.
            </span>
          </h1>

          <p className="text-slate-400 text-base sm:text-lg leading-relaxed">
            Transforming standard refrigeration with universal computer vision recognition, 
            predictive consumption learning, expiry alerts, and authorized automatic restocking.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              to="/register"
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 font-semibold text-sm text-white shadow-lg shadow-cyan-500/25 transition flex items-center gap-2"
            >
              <span>Create Virtual Refrigerator</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              to="/login"
              className="px-6 py-3 rounded-xl border border-slate-700 bg-slate-900/80 hover:bg-slate-800 font-medium text-sm text-slate-200 transition"
            >
              Sign In to Your Fridge
            </Link>
          </div>
        </div>
      </section>

      {/* Live System Health Diagnostic Banner */}
      <section className="p-6 rounded-2xl border border-slate-800/80 bg-slate-900/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Activity className="h-5 w-5" />
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Live Cloud Health Check</div>
              <div className="text-xs text-slate-400">
                Connected to FastAPI production backend
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            {loading ? (
              <span className="text-slate-400">Probing cloud backend...</span>
            ) : error ? (
              <span className="text-rose-400 flex items-center gap-1.5">
                <AlertCircle className="h-4 w-4" /> Disconnected: {error}
              </span>
            ) : healthData ? (
              <span className="text-emerald-400 flex items-center gap-1.5 bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-800/50">
                <CheckCircle2 className="h-4 w-4" /> Operational: {healthData.service} v{healthData.version}
              </span>
            ) : null}
          </div>
        </div>
      </section>

      {/* 6 Core Pillars Grid */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Designed for Modern Household Intelligence
          </h2>
          <p className="text-sm text-slate-400">
            A comprehensive suite of intelligent tools managing groceries, medicines, cosmetics, and prepared food.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <div 
              key={i} 
              className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 hover:border-slate-700/80 transition space-y-3"
            >
              <div className="h-10 w-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                <f.icon className="h-5 w-5" />
              </div>
              <h3 className="text-base font-semibold text-white">{f.title}</h3>
              <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
