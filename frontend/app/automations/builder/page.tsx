"use client";

import { useState, useCallback } from "react";
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";
import { Zap, Clock, TrendingUp, Send, MessageSquare, Plus } from "lucide-react";

const nodeTypes = {
  trigger: TriggerNode,
  condition: ConditionNode,
  action: ActionNode,
};

function TriggerNode({ data }: any) {
  return (
    <div className="px-4 py-3 rounded-xl bg-brand-primary text-white shadow-lg border-2 border-brand-primary-dark min-w-[200px]">
      <div className="flex items-center gap-2 mb-2">
        <Zap size={16} />
        <span className="text-xs font-semibold uppercase">Trigger</span>
      </div>
      <p className="text-sm font-medium">{data.label}</p>
    </div>
  );
}

function ConditionNode({ data }: any) {
  return (
    <div className="px-4 py-3 rounded-xl bg-warning text-white shadow-lg border-2 border-warning-dark min-w-[200px]">
      <div className="flex items-center gap-2 mb-2">
        <TrendingUp size={16} />
        <span className="text-xs font-semibold uppercase">Condition</span>
      </div>
      <p className="text-sm font-medium">{data.label}</p>
    </div>
  );
}

function ActionNode({ data }: any) {
  return (
    <div className="px-4 py-3 rounded-xl bg-brand-secondary text-white shadow-lg border-2 border-brand-secondary-dark min-w-[200px]">
      <div className="flex items-center gap-2 mb-2">
        <Send size={16} />
        <span className="text-xs font-semibold uppercase">Action</span>
      </div>
      <p className="text-sm font-medium">{data.label}</p>
    </div>
  );
}

const initialNodes: Node[] = [
  {
    id: "1",
    type: "trigger",
    data: { label: "New Follower" },
    position: { x: 250, y: 100 },
  },
];

const initialEdges: Edge[] = [];

export default function AutomationBuilderPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNodeType, setSelectedNodeType] = useState<string | null>(null);

  const onConnect = useCallback(
    (params: Connection) =>
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            animated: true,
            markerEnd: { type: MarkerType.ArrowClosed },
          },
          eds
        )
      ),
    [setEdges]
  );

  const addNode = (type: string, label: string) => {
    const newNode: Node = {
      id: `${nodes.length + 1}`,
      type,
      data: { label },
      position: { x: 250, y: 100 + nodes.length * 150 },
    };
    setNodes([...nodes, newNode]);
  };

  return (
    <div className="h-screen flex flex-col">
      <header className="bg-surface border-b border-muted p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Automation Builder</h1>
            <p className="text-sm text-muted">Drag, drop, connect - stile n8n</p>
          </div>
          <div className="flex gap-2">
            <button className="btn-secondary">Salva Bozza</button>
            <button className="btn-primary">Attiva Automation</button>
          </div>
        </div>
      </header>

      <div className="flex-1 flex">
        <aside className="w-64 bg-surface border-r border-muted p-4 overflow-y-auto">
          <h3 className="text-sm font-semibold text-foreground mb-3">Aggiungi Nodo</h3>

          <div className="space-y-2 mb-4">
            <p className="text-xs text-muted font-medium uppercase">Triggers</p>
            <button
              onClick={() => addNode("trigger", "Nuovo Follower")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <Zap size={16} className="text-brand-primary" />
                <span className="text-sm font-medium text-foreground">Nuovo Follower</span>
              </div>
              <p className="text-xs text-muted">Quando qualcuno ti segue</p>
            </button>
            <button
              onClick={() => addNode("trigger", "Schedule")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <Clock size={16} className="text-brand-primary" />
                <span className="text-sm font-medium text-foreground">Schedule</span>
              </div>
              <p className="text-xs text-muted">Giorno/ora specifica</p>
            </button>
            <button
              onClick={() => addNode("trigger", "Engagement < X%")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <TrendingUp size={16} className="text-brand-primary" />
                <span className="text-sm font-medium text-foreground">Soglia Engagement</span>
              </div>
              <p className="text-xs text-muted">Quando metric scende</p>
            </button>
          </div>

          <div className="space-y-2 mb-4">
            <p className="text-xs text-muted font-medium uppercase">Conditions</p>
            <button
              onClick={() => addNode("condition", "Se X allora Y")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <TrendingUp size={16} className="text-warning" />
                <span className="text-sm font-medium text-foreground">Condizione If/Else</span>
              </div>
              <p className="text-xs text-muted">Logica condizionale</p>
            </button>
          </div>

          <div className="space-y-2">
            <p className="text-xs text-muted font-medium uppercase">Actions</p>
            <button
              onClick={() => addNode("action", "Crea Draft")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <Plus size={16} className="text-brand-secondary" />
                <span className="text-sm font-medium text-foreground">Crea Draft</span>
              </div>
              <p className="text-xs text-muted">Bozza post da template</p>
            </button>
            <button
              onClick={() => addNode("action", "Invia Notifica")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <Send size={16} className="text-brand-secondary" />
                <span className="text-sm font-medium text-foreground">Notifica</span>
              </div>
              <p className="text-xs text-muted">Email/Slack/webhook</p>
            </button>
            <button
              onClick={() => addNode("action", "Richiedi Approvazione")}
              className="w-full p-3 rounded-lg bg-background hover:bg-muted transition-colors text-left border border-muted"
            >
              <div className="flex items-center gap-2 mb-1">
                <MessageSquare size={16} className="text-brand-secondary" />
                <span className="text-sm font-medium text-foreground">Approval</span>
              </div>
              <p className="text-xs text-muted">Manual review step</p>
            </button>
          </div>
        </aside>

        <main className="flex-1 bg-background">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </main>
      </div>
    </div>
  );
}
