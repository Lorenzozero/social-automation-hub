"use client";

import { useState } from "react";
import { ChevronRight, CheckCircle, Sparkles, Calendar, Zap } from "lucide-react";
import { useRouter } from "next/navigation";

const steps = [
  {
    id: 1,
    title: "Connect Your First Account",
    description: "Link your social media account to start managing your content",
    icon: Sparkles,
  },
  {
    id: 2,
    title: "Schedule Your First Post",
    description: "Create and schedule your first piece of content",
    icon: Calendar,
  },
  {
    id: 3,
    title: "Set Up an Automation",
    description: "Automate repetitive tasks and save time",
    icon: Zap,
  },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);

  const handleStepComplete = () => {
    if (!completedSteps.includes(currentStep)) {
      setCompletedSteps([...completedSteps, currentStep]);
    }
    
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    } else {
      // Onboarding complete
      router.push("/dashboard");
    }
  };

  const handleSkip = () => {
    router.push("/dashboard");
  };

  const currentStepData = steps[currentStep - 1];
  const Icon = currentStepData.icon;

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-brand-primary/10 to-brand-secondary/10">
      <div className="max-w-2xl w-full space-y-8">
        {/* Progress Indicator */}
        <div className="flex items-center justify-center gap-2">
          {steps.map((step) => (
            <div key={step.id} className="flex items-center gap-2">
              <div
                className={`h-10 w-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all ${
                  completedSteps.includes(step.id)
                    ? "bg-success text-white"
                    : step.id === currentStep
                    ? "bg-brand-primary text-white scale-110"
                    : "bg-surface text-muted"
                }`}
              >
                {completedSteps.includes(step.id) ? (
                  <CheckCircle size={20} />
                ) : (
                  step.id
                )}
              </div>
              {step.id < steps.length && (
                <div
                  className={`h-1 w-12 rounded-full transition-all ${
                    completedSteps.includes(step.id)
                      ? "bg-success"
                      : "bg-muted"
                  }`}
                ></div>
              )}
            </div>
          ))}
        </div>

        {/* Step Content */}
        <div className="card text-center space-y-6 animate-fade-in">
          <div className="h-20 w-20 rounded-full bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center mx-auto">
            <Icon size={40} className="text-white" />
          </div>
          
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-2">
              {currentStepData.title}
            </h2>
            <p className="text-muted">{currentStepData.description}</p>
          </div>

          <div className="space-y-4 pt-4">
            {currentStep === 1 && (
              <div className="grid grid-cols-2 gap-4">
                {["Instagram", "TikTok", "LinkedIn", "X"].map((platform) => (
                  <button
                    key={platform}
                    onClick={handleStepComplete}
                    className="p-4 rounded-xl bg-surface hover:bg-muted transition-colors text-left border-2 border-transparent hover:border-brand-primary"
                  >
                    <p className="text-sm font-semibold text-foreground">{platform}</p>
                    <p className="text-xs text-muted">Connect account</p>
                  </button>
                ))}
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-3 text-left">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Post Title
                  </label>
                  <input
                    type="text"
                    placeholder="My first post"
                    className="w-full px-4 py-3 bg-surface border border-muted rounded-xl focus:ring-2 focus:ring-brand-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Caption
                  </label>
                  <textarea
                    placeholder="Write your caption..."
                    rows={4}
                    className="w-full px-4 py-3 bg-surface border border-muted rounded-xl focus:ring-2 focus:ring-brand-primary focus:outline-none resize-none"
                  />
                </div>
                <button onClick={handleStepComplete} className="btn-primary w-full">
                  Schedule Post
                </button>
              </div>
            )}

            {currentStep === 3 && (
              <div className="grid grid-cols-1 gap-3">
                {[
                  "Welcome new followers with auto-DM",
                  "Post motivational quote every Monday",
                  "Alert me when engagement drops",
                ].map((automation, idx) => (
                  <button
                    key={idx}
                    onClick={handleStepComplete}
                    className="p-4 rounded-xl bg-surface hover:bg-muted transition-colors text-left border-2 border-transparent hover:border-brand-primary"
                  >
                    <p className="text-sm font-semibold text-foreground">{automation}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between">
          <button onClick={handleSkip} className="text-sm text-muted hover:text-foreground">
            Skip onboarding
          </button>
          <div className="text-sm text-muted">
            Step {currentStep} of {steps.length}
          </div>
        </div>
      </div>
    </div>
  );
}
