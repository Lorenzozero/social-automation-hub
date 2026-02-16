"use client";

import { useState } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";

interface AutomationNode {
  id: string;
  type: "trigger" | "condition" | "action";
  config: any;
}

const TRIGGERS = [
  { id: "new_post", label: "New Post Published", icon: "📝" },
  { id: "new_follower", label: "New Follower", icon: "👤" },
  { id: "mention", label: "Mentioned in Post", icon: "@" },
  { id: "kpi_threshold", label: "KPI Threshold Reached", icon: "📊" },
];

const ACTIONS = [
  { id: "create_draft", label: "Create Draft Post", icon: "✍️" },
  { id: "send_notification", label: "Send Notification", icon: "🔔" },
  { id: "request_approval", label: "Request Approval", icon: "✅" },
  { id: "add_to_calendar", label: "Add to Calendar", icon: "📅" },
];

export default function AutomationBuilderPage() {
  const [nodes, setNodes] = useState<AutomationNode[]>([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const addNode = (type: "trigger" | "action", config: any) => {
    const newNode: AutomationNode = {
      id: `${type}_${Date.now()}`,
      type,
      config,
    };
    setNodes([...nodes, newNode]);
  };

  const onDragEnd = (result: any) => {
    if (!result.destination) return;
    
    const items = Array.from(nodes);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    
    setNodes(items);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          Automation Builder
        </h1>
        <p className="text-sm text-muted mt-2">Build workflows with drag-and-drop triggers and actions</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Palette */}
        <div className="card space-y-4">
          <h3 className="text-sm font-semibold text-foreground">Triggers</h3>
          <div className="space-y-2">
            {TRIGGERS.map((trigger) => (
              <button
                key={trigger.id}
                onClick={() => addNode("trigger", { type: trigger.id })}
                className="w-full p-3 rounded-xl bg-surface hover:bg-muted transition flex items-center gap-3 text-left"
              >
                <span className="text-2xl">{trigger.icon}</span>
                <span className="text-sm font-medium text-foreground">{trigger.label}</span>
              </button>
            ))}
          </div>

          <h3 className="text-sm font-semibold text-foreground mt-6">Actions</h3>
          <div className="space-y-2">
            {ACTIONS.map((action) => (
              <button
                key={action.id}
                onClick={() => addNode("action", { type: action.id })}
                className="w-full p-3 rounded-xl bg-surface hover:bg-muted transition flex items-center gap-3 text-left"
              >
                <span className="text-2xl">{action.icon}</span>
                <span className="text-sm font-medium text-foreground">{action.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Canvas */}
        <div className="lg:col-span-2 card min-h-[600px]">
          <h3 className="text-sm font-semibold text-foreground mb-4">Workflow</h3>
          {nodes.length === 0 ? (
            <div className="flex items-center justify-center h-full text-muted">
              <p>Drag triggers and actions from the left to build your workflow</p>
            </div>
          ) : (
            <DragDropContext onDragEnd={onDragEnd}>
              <Droppable droppableId="workflow">
                {(provided) => (
                  <div
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                    className="space-y-3"
                  >
                    {nodes.map((node, index) => (
                      <Draggable key={node.id} draggableId={node.id} index={index}>
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="p-4 rounded-xl bg-surface border-2 border-transparent hover:border-brand-primary transition cursor-move"
                            onClick={() => setSelectedNode(node.id)}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                <span className="text-2xl">⋮⋮</span>
                                <div>
                                  <p className="text-sm font-semibold text-foreground">
                                    {node.type === "trigger" ? "Trigger" : "Action"}: {node.config.type}
                                  </p>
                                  <p className="text-xs text-muted">Click to configure</p>
                                </div>
                              </div>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setNodes(nodes.filter((n) => n.id !== node.id));
                                }}
                                className="text-red-500 hover:text-red-700"
                              >
                                🗑️
                              </button>
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </DragDropContext>
          )}

          {nodes.length > 0 && (
            <div className="mt-6 flex gap-3">
              <button className="btn-primary">Save Automation</button>
              <button className="btn-secondary">Test Run</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
