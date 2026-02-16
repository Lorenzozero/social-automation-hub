"use client";

import { usePreferences } from "@/store/preferences";
import enLocale from "@/locales/en.json";
import itLocale from "@/locales/it.json";

const locales = { en: enLocale.en, it: itLocale.it };

export function useTranslations() {
  const locale = usePreferences((s) => s.locale);
  const messages = locales[locale];

  return (key: string) => {
    const keys = key.split(".");
    let value: any = messages;
    for (const k of keys) {
      value = value?.[k];
    }
    return value || key;
  };
}
