"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

interface Message {
  id: string;
  platform: string;
  type: "comment" | "dm";
  from_user: string;
  from_user_pic?: string;
  text: string;
  timestamp: string;
  post_id?: string;
  sentiment?: "positive" | "negative" | "neutral";
  priority?: "high" | "medium" | "low";
}

export default function InboxPage() {
  const searchParams = useSearchParams();
  const [messages, setMessages] = useState<Message[]>([]);
  const [filter, setFilter] = useState<"all" | "comments" | "dms">("all");
  const [selectedMessage, setSelectedMessage] = useState<Message | null>(null);
  const [replyText, setReplyText] = useState("");

  useEffect(() => {
    // Mock data - replace with real API call
    const mockMessages: Message[] = [
      {
        id: "1",
        platform: "instagram",
        type: "comment",
        from_user: "user123",
        text: "Love this content! 🔥",
        timestamp: new Date().toISOString(),
        sentiment: "positive",
        priority: "low",
      },
      {
        id: "2",
        platform: "x",
        type: "comment",
        from_user: "twitteruser",
        text: "This is terrible advice.",
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        sentiment: "negative",
        priority: "high",
      },
    ];
    setMessages(mockMessages);
  }, [filter]);

  const filteredMessages = messages.filter((msg) => {
    if (filter === "all") return true;
    return msg.type === filter.slice(0, -1);
  });

  const handleReply = () => {
    if (!selectedMessage || !replyText.trim()) return;
    // API call to send reply
    console.log("Replying to", selectedMessage.id, ":", replyText);
    setReplyText("");
    setSelectedMessage(null);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            Unified Inbox
          </h1>
          <p className="text-sm text-muted mt-2">Manage comments and DMs from all platforms</p>
        </div>
        <div className="flex gap-2">
          {["all", "comments", "dms"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f as any)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                filter === f ? "bg-brand-primary text-white" : "bg-surface text-muted hover:bg-muted"
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Message list */}
        <div className="lg:col-span-2 card max-h-[700px] overflow-y-auto space-y-3">
          {filteredMessages.length === 0 ? (
            <p className="text-muted text-center py-12">No messages</p>
          ) : (
            filteredMessages.map((msg) => (
              <div
                key={msg.id}
                onClick={() => setSelectedMessage(msg)}
                className={`p-4 rounded-xl cursor-pointer transition ${
                  selectedMessage?.id === msg.id
                    ? "bg-brand-primary/10 border-2 border-brand-primary"
                    : "bg-surface hover:bg-muted"
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-white font-bold">
                      {msg.from_user[0].toUpperCase()}
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-foreground">@{msg.from_user}</p>
                      <p className="text-xs text-muted capitalize">{msg.platform} · {msg.type}</p>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    msg.priority === "high" ? "bg-red-500/20 text-red-500" :
                    msg.priority === "medium" ? "bg-yellow-500/20 text-yellow-500" :
                    "bg-green-500/20 text-green-500"
                  }`}>
                    {msg.priority}
                  </span>
                </div>
                <p className="text-sm text-foreground">{msg.text}</p>
                <p className="text-xs text-muted mt-2">{new Date(msg.timestamp).toLocaleString()}</p>
              </div>
            ))
          )}
        </div>

        {/* Reply panel */}
        <div className="card">
          {!selectedMessage ? (
            <p className="text-muted text-center py-12">Select a message to reply</p>
          ) : (
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-semibold text-foreground mb-2">Reply to @{selectedMessage.from_user}</h3>
                <p className="text-sm text-muted">{selectedMessage.text}</p>
              </div>
              <textarea
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder="Type your reply..."
                className="w-full h-32 p-3 rounded-xl bg-surface text-foreground text-sm resize-none focus:outline-none focus:ring-2 focus:ring-brand-primary"
              />
              <div className="flex gap-2">
                <button onClick={handleReply} className="btn-primary flex-1">Send Reply</button>
                <button className="btn-secondary">AI Suggest</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
