import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, Timer, Send, AlertOctagon, Zap, Bell, Bot, Terminal, Volume2, VolumeX, Moon, Sun, RefreshCw } from 'lucide-react';
import { sound } from './utils/audio';

export default function App() {
  const [isDark, setIsDark] = useState(true);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [metrics, setMetrics] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    sound.enabled = soundEnabled;
  }, [soundEnabled]);

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const res = await fetch('/api/metrics/summary');
        if (res.ok) setMetrics(await res.json());
      } catch (e) {}
    };
    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 3000);
    return () => clearInterval(interval);
  }, []);

  const triggerSimulation = async (scenarioId: string) => {
    sound.playClick();
    try {
      const res = await fetch('/api/simulations/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario_id: scenarioId })
      });
      if (res.ok) {
        sound.playSuccess();
        const updated = await fetch('/api/metrics/summary');
        if (updated.ok) setMetrics(await updated.json());
      } else {
        sound.playError();
      }
    } catch (e) {
      sound.playError();
    }
  };

  return (
    <div className={`min-h-screen ${isDark ? 'dark bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'} antialiased transition-colors duration-300`}>
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-white/10 backdrop-blur-md bg-slate-900/70 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Activity className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h1 className="font-bold text-base sm:text-lg">Antigravity Observability</h1>
            <p className="text-xs text-slate-400">FastAPI Real-Time Telemetry & Chaos Sandbox</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className={`px-3 py-1 rounded-full text-xs font-semibold border ${
            metrics?.service_status === 'Healthy' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
            metrics?.service_status === 'Degraded' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
            'bg-rose-500/10 text-rose-400 border-rose-500/20'
          }`}>
            {metrics?.service_status || 'Connecting...'}
          </div>

          <button onClick={() => { setSoundEnabled(!soundEnabled); sound.playClick(); }} className="p-2 rounded-lg border border-white/10 hover:bg-white/5">
            {soundEnabled ? <Volume2 className="w-4 h-4 text-cyan-400" /> : <VolumeX className="w-4 h-4 text-slate-400" />}
          </button>

          <button onClick={() => { setIsDark(!isDark); sound.playClick(); }} className="p-2 rounded-lg border border-white/10 hover:bg-white/5">
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-700" />}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
        {/* Metric Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-md">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span>API Uptime</span>
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-3xl font-extrabold">{metrics?.uptime_percent ?? '--'}%</div>
            <div className="text-xs text-emerald-400 mt-2">Target 99.9% SLA</div>
          </div>

          <div className="p-5 rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-md">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span>Avg Latency</span>
              <Timer className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="text-3xl font-extrabold">{metrics?.avg_response_time_ms ?? '--'} ms</div>
            <div className="text-xs text-slate-400 mt-2">p95: {metrics?.p95_response_time_ms ?? '--'} ms</div>
          </div>

          <div className="p-5 rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-md">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span>Total Requests</span>
              <Send className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-3xl font-extrabold">{metrics?.total_requests ?? '--'}</div>
            <div className="text-xs text-cyan-400 mt-2">{metrics?.requests_per_minute ?? 0} Requests/Min</div>
          </div>

          <div className="p-5 rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-md">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span>Failed Requests</span>
              <AlertOctagon className="w-4 h-4 text-rose-400" />
            </div>
            <div className="text-3xl font-extrabold text-rose-400">{metrics?.failed_requests ?? '--'}</div>
            <div className="text-xs text-rose-400 mt-2">{metrics?.error_rate_percent ?? 0}% Error Rate</div>
          </div>
        </div>

        {/* Simulation Bar */}
        <div className="p-6 rounded-2xl border border-cyan-500/20 bg-gradient-to-r from-cyan-950/30 via-slate-900/50 to-indigo-950/30">
          <h2 className="text-sm font-bold flex items-center gap-2 mb-1">
            <Zap className="w-4 h-4 text-cyan-400" /> Chaos & Failure Simulations
          </h2>
          <p className="text-xs text-slate-400 mb-4">Validate alerts, RCA generation, and audio feedback by triggering live failure scenarios:</p>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <button onClick={() => triggerSimulation('auth_failure')} className="p-3 rounded-xl border border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20 text-xs font-semibold text-amber-300">
              1. Auth Failure (401)
            </button>
            <button onClick={() => triggerSimulation('timeout')} className="p-3 rounded-xl border border-yellow-500/30 bg-yellow-500/10 hover:bg-yellow-500/20 text-xs font-semibold text-yellow-300">
              2. API Timeout (&gt;3s)
            </button>
            <button onClick={() => triggerSimulation('server_error')} className="p-3 rounded-xl border border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/20 text-xs font-semibold text-rose-300">
              3. Server Crash (500)
            </button>
            <button onClick={() => triggerSimulation('rate_limit')} className="p-3 rounded-xl border border-purple-500/30 bg-purple-500/10 hover:bg-purple-500/20 text-xs font-semibold text-purple-300">
              4. Rate Limit (429)
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

