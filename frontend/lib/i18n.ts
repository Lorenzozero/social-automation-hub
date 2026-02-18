"use client";

import { usePreferences } from "@/store/preferences";
import en from "@/locales/en.json";

type TranslationKey = string;

export function useTranslations() {
  const { language } = usePreferences();
  
  return (key: TranslationKey): string => {
    const keys = key.split('.');
    let value: any = en;
    
    for (const k of keys) {
      value = value?.[k];
      if (!value) return key;
    }
    
    return value || key;
  };
}

export function getTranslations(locale: string = 'en') {
  return en;
}
