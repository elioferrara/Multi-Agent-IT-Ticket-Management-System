import { CopilotChat } from "@copilotkit/react-core/v2"; 

export default function Page() {
 return (
    <main className="flex h-screen w-full items-center justify-center bg-gradient-to-tr from-zinc-950 via-slate-900 to-indigo-950 p-4 font-sans">
      
      <div className="flex h-[88vh] w-full max-w-4xl flex-col rounded-2xl border border-white/10 bg-zinc-950/40 shadow-2xl backdrop-blur-xl overflow-hidden">
        
        <div className="p-6 text-center border-b border-white/5 bg-white/[0.02]">
          <h1 className="text-2xl font-bold tracking-tight text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.15)]">
            Gestione Ticket
          </h1>
          <p className="text-[10px] text-zinc-400 mt-1.5 font-bold uppercase tracking-[0.2em] opacity-80">
            SISTEMA MULTI AGENTE PER LA GESTIONE DI TICKET AZIENDALI
          </p>
        </div>

        <div className="flex-1 overflow-hidden bg-transparent">
          <CopilotChat/>
        </div>

      </div>
      
    </main>
  );
}
