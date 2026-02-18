"use client";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-card border-t border-border py-6 px-6 mt-auto">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="text-sm text-muted">
              © {currentYear} SocialHub. Built with ❤️ by Lorenzo.
            </p>
          </div>
          <div className="flex gap-6">
            <a
              href="/privacy"
              className="text-sm text-muted hover:text-foreground transition-colors"
            >
              Privacy
            </a>
            <a
              href="/terms"
              className="text-sm text-muted hover:text-foreground transition-colors"
            >
              Terms
            </a>
            <a
              href="/docs"
              className="text-sm text-muted hover:text-foreground transition-colors"
            >
              Docs
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
