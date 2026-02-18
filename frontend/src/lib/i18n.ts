"use client";

import { usePreferences } from "@/store/preferences";
import enLocale from "@/locales/en.json";
import itLocale from "@/locales/it.json";

type Locale = 'en' | 'it';

const locales: Record<Locale, any> = {
  en: enLocale,
  it: itLocale,
};

export function useTranslations() {
  const language = usePreferences((s) => s.language);
  const messages = locales[language as Locale] || locales.en;

  return (key: string) => {
    const keys = key.split(".");
    let value: any = messages;
    for (const k of keys) {
      value = value?.[k];
    }
    return value || key;
  };
}

export function getTranslations(locale: Locale = 'en') {
  return locales[locale] || locales.en;
}
