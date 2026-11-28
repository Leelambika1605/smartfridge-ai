import React from 'react';
import { 
  Refrigerator as FridgeIcon, 
  Thermometer, 
  Layers, 
  PlusCircle, 
  Sparkles, 
  Clock, 
  ShoppingCart, 
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  TrendingDown,
  Activity
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user, activeFridge } = useAuth();

  const mockCategories = [
    { name: "Groceries", count: 14, icon: "🥛", color: "from-emerald-500/20 to-emerald-600/10 border-emerald-500/30 text-emerald-300" },
    { name: "Beverages", count: 8, icon: "🧃", color: "from-blue-500/20 to-blue-600/10 border-blue-500/30 text-blue-300" },
    { name: "Medicines", count: 2, icon: "💉", color: "from-rose-500/20 to-rose-600/10 border-rose-500/30 text-rose-300" },
    { name: "Skincare", count: 4, icon: "✨", color: "from-purple-500/20 to-purple-600/10 border-purple-500/30 text-purple-300" },
    { name: "Prepared Food", count: 3, icon: "🍲", color: "from-amber-500/20 to-amber-600/10 border-amber-500/30 text-amber-300" },
    { name: "Other Items", count: 1, icon: "📦", color: "from-slate-500/20 to-slate-600/10 border-slate-500/30 text-slate-300" },
  ];

  return (
    <div className="space-y-8 py-6">
      
      {/* Top Welcome Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 sm:p-8 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-slate-950">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800 text-cyan-300 text-xs font-semibold">
            <Sparkles className="h-3.5 w-3.5" />
            Active Household Manager
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Welcome back, {user?.full_name || 'Chef'}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Monitoring refrigerator contents, consumption trends, and automated replenishment.
          </p>
        </div>

        {/* Active Fridge Indicator Pill */}
        {activeFridge && (
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950 border border-slate-800 shrink-0">
            <div className="h-10 w-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <FridgeIcon className="h-5 w-5" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Assigned Virtual Appliance</div>
              <div className="text-sm font-bold text-white">{activeFridge.name}</div>
              <div className="text-[10px] text-cyan-400 font-mono">
                Location: {activeFridge.location || 'Kitchen'} • Target: {activeFridge.target_temperature_celsius}°C
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Real-time Status Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Total Items */}
        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Items</span>
            <Layers className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">32</div>
          <div className="text-xs text-emerald-400 flex items-center gap-1 font-medium">
            <CheckCircle2 className="h-3.5 w-3.5" /> 28 in healthy stock
          </div>
        </div>

        {/* Low Stock Warning */}
        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Low Stock</span>
            <TrendingDown className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400">3</div>
          <div className="text-xs text-slate-400">
            Milk, Butter, Orange Juice
          </div>
        </div>

        {/* Expiry Radar */}
        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Expiring in 48h</span>
            <Clock className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-rose-400">1</div>
          <div className="text-xs text-rose-300/80 font-medium flex items-center gap-1">
            <AlertTriangle className="h-3.5 w-3.5" /> Greek Yogurt (expires tomorrow)
          </div>
        </div>

        {/* Target Temp */}
        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Storage Temp</span>
            <Thermometer className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-cyan-300">
            {activeFridge?.target_temperature_celsius || 3.5}°C
          </div>
          <div className="text-xs text-emerald-400 font-medium">
            Optimal safe range (1°C - 4°C)
          </div>
        </div>

      </div>

      {/* 6 Category Breakdown */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="h-5 w-5 text-cyan-400" />
            Universal Category Inventory
          </h2>
          <span className="text-xs text-slate-400">6 Storage Categories</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {mockCategories.map((c, i) => (
            <div
              key={i}
              className={`p-4 rounded-2xl border bg-gradient-to-b ${c.color} space-y-2 transition hover:scale-102`}
            >
              <div className="text-2xl">{c.icon}</div>
              <div className="text-xs font-semibold text-slate-200">{c.name}</div>
              <div className="text-lg font-extrabold text-white">{c.count} items</div>
            </div>
          ))}
        </div>
      </div>

      {/* Next Up Phase Banner */}
      <div className="p-6 rounded-2xl border border-cyan-800/40 bg-gradient-to-r from-cyan-950/40 to-blue-950/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="text-sm font-bold text-white flex items-center gap-2">
            <Activity className="h-4 w-4 text-cyan-400" />
            Module 1 Authentication Complete!
          </div>
          <p className="text-xs text-slate-400">
            User multi-tenancy active. Each account now maintains its own isolated virtual refrigerator and data.
          </p>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 text-xs font-semibold">
          Ready for Inventory & AI Vision
        </div>
      </div>

    </div>
  );
}
