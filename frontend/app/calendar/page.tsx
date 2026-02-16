"use client";

import { useState, useEffect } from "react";
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight } from "lucide-react";
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay, addMonths, subMonths, startOfWeek, endOfWeek } from "date-fns";

interface Post {
  id: string;
  title: string;
  scheduled_at: string;
  platform: string;
  status: string;
}

const platformColors: Record<string, string> = {
  instagram: "bg-gradient-to-br from-purple-500 to-pink-500",
  tiktok: "bg-gradient-to-br from-cyan-500 to-pink-500",
  linkedin: "bg-blue-600",
  x: "bg-gray-900",
};

export default function CalendarPage() {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [posts, setPosts] = useState<Post[]>([
    {
      id: "1",
      title: "Monday Motivation",
      scheduled_at: "2026-02-16T08:00:00Z",
      platform: "instagram",
      status: "scheduled",
    },
    {
      id: "2",
      title: "Product Launch",
      scheduled_at: "2026-02-18T15:00:00Z",
      platform: "linkedin",
      status: "scheduled",
    },
    {
      id: "3",
      title: "Behind the Scenes",
      scheduled_at: "2026-02-20T19:00:00Z",
      platform: "tiktok",
      status: "scheduled",
    },
  ]);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const calendarStart = startOfWeek(monthStart);
  const calendarEnd = endOfWeek(monthEnd);
  const calendarDays = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

  const getPostsForDay = (day: Date) => {
    return posts.filter((post) => {
      const postDate = new Date(post.scheduled_at);
      return isSameDay(postDate, day);
    });
  };

  const handlePrevMonth = () => setCurrentMonth(subMonths(currentMonth, 1));
  const handleNextMonth = () => setCurrentMonth(addMonths(currentMonth, 1));

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <section className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            Content Calendar
          </h1>
          <p className="text-sm text-muted">Plan and schedule your content across platforms</p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <CalendarIcon size={20} />
          Schedule Post
        </button>
      </section>

      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-foreground">
            {format(currentMonth, "MMMM yyyy")}
          </h2>
          <div className="flex gap-2">
            <button
              onClick={handlePrevMonth}
              className="p-2 rounded-lg bg-surface hover:bg-muted transition-colors"
            >
              <ChevronLeft size={20} />
            </button>
            <button
              onClick={() => setCurrentMonth(new Date())}
              className="px-4 py-2 rounded-lg bg-surface hover:bg-muted transition-colors text-sm font-medium"
            >
              Today
            </button>
            <button
              onClick={handleNextMonth}
              className="p-2 rounded-lg bg-surface hover:bg-muted transition-colors"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </div>

        {/* Calendar Grid */}
        <div className="grid grid-cols-7 gap-2">
          {/* Day headers */}
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
            <div
              key={day}
              className="text-center text-xs font-semibold text-muted py-2"
            >
              {day}
            </div>
          ))}

          {/* Calendar days */}
          {calendarDays.map((day, idx) => {
            const dayPosts = getPostsForDay(day);
            const isCurrentMonth = isSameMonth(day, currentMonth);
            const isToday = isSameDay(day, new Date());
            const isSelected = selectedDate && isSameDay(day, selectedDate);

            return (
              <button
                key={idx}
                onClick={() => setSelectedDate(day)}
                className={`min-h-[100px] p-2 rounded-xl border transition-all ${
                  isCurrentMonth
                    ? "bg-background border-muted hover:border-brand-primary"
                    : "bg-surface border-transparent text-muted"
                } ${
                  isToday ? "ring-2 ring-brand-primary" : ""
                } ${
                  isSelected ? "border-brand-primary bg-brand-primary/5" : ""
                }`}
              >
                <div className="text-sm font-medium mb-2">
                  {format(day, "d")}
                </div>
                <div className="space-y-1">
                  {dayPosts.map((post) => (
                    <div
                      key={post.id}
                      className={`text-xs p-1 rounded text-white truncate ${
                        platformColors[post.platform]
                      }`}
                      title={post.title}
                    >
                      {post.title}
                    </div>
                  ))}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Selected Day Details */}
      {selectedDate && (
        <div className="card animate-fade-in">
          <h3 className="text-lg font-semibold text-foreground mb-4">
            {format(selectedDate, "EEEE, MMMM d, yyyy")}
          </h3>
          {getPostsForDay(selectedDate).length > 0 ? (
            <div className="space-y-3">
              {getPostsForDay(selectedDate).map((post) => (
                <div
                  key={post.id}
                  className="flex items-center justify-between p-4 rounded-xl bg-surface"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`h-10 w-10 rounded-lg ${platformColors[post.platform]} flex items-center justify-center text-white font-semibold text-sm`}
                    >
                      {post.platform[0].toUpperCase()}
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-foreground">{post.title}</p>
                      <p className="text-xs text-muted">
                        {format(new Date(post.scheduled_at), "h:mm a")} · {post.platform}
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="btn-secondary text-xs">Edit</button>
                    <button className="btn-primary text-xs">View</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-sm text-muted mb-3">No posts scheduled for this day</p>
              <button className="btn-primary text-sm">Schedule Post</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
