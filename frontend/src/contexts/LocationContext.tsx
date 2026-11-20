'use client';

import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import { RegionItem } from '@/types';
import { fetchRegionsApi, locateRegionApi } from '@/lib/api';

const STORAGE_KEY = 'agro_selected_province';

interface LocationContextValue {
  provinceCode: string; // 'all' | 'khanh-hoa' | 'dak-lak' | ...
  provinceName: string;
  selectedRegionObj: RegionItem | null;
  regions: RegionItem[];
  loadingRegions: boolean;
  locating: boolean;
  locateFeedback: { type: 'success' | 'error'; text: string } | null;
  setProvinceCode: (code: string) => void;
  detectMyLocation: () => Promise<boolean>;
  clearLocateFeedback: () => void;
}

const LocationContext = createContext<LocationContextValue | undefined>(undefined);

export function LocationProvider({ children }: { children: React.ReactNode }) {
  const [provinceCode, setProvinceCodeState] = useState<string>('all');
  const [regions, setRegions] = useState<RegionItem[]>([]);
  const [loadingRegions, setLoadingRegions] = useState<boolean>(true);
  const [locating, setLocating] = useState<boolean>(false);
  const [locateFeedback, setLocateFeedback] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Hydrate persisted province from localStorage safely on client
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved && saved.trim()) {
        setProvinceCodeState(saved.trim());
      }
    } catch {
      // Ignore storage access restrictions
    }
  }, []);

  // Load supported provinces & direct-survey coverage once
  useEffect(() => {
    let active = true;
    fetchRegionsApi()
      .then((list) => {
        if (active && Array.isArray(list)) {
          setRegions(list);
        }
      })
      .catch(() => {
        // Keep graceful empty list if offline
      })
      .finally(() => {
        if (active) setLoadingRegions(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const setProvinceCode = useCallback((code: string) => {
    const next = code && code.trim() ? code.trim() : 'all';
    setProvinceCodeState(next);
    setLocateFeedback(null);
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // Ignore storage errors
    }
  }, []);

  const clearLocateFeedback = useCallback(() => {
    setLocateFeedback(null);
  }, []);

  const detectMyLocation = useCallback(async (): Promise<boolean> => {
    if (typeof window === 'undefined' || !('geolocation' in navigator)) {
      setLocateFeedback({
        type: 'error',
        text: 'Trình duyệt của bạn không hỗ trợ định vị GPS. Vui lòng chọn tỉnh thủ công.',
      });
      return false;
    }

    setLocating(true);
    setLocateFeedback(null);

    try {
      const pos = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: false,
          timeout: 10000,
          maximumAge: 300000,
        });
      });

      const located = await locateRegionApi(pos.coords.latitude, pos.coords.longitude);
      setProvinceCodeState(located.province_code);
      try {
        window.localStorage.setItem(STORAGE_KEY, located.province_code);
      } catch {
        // Ignore storage errors
      }
      setLocateFeedback({
        type: 'success',
        text: `Đã định vị: ${located.province_name} (${located.region_name})`,
      });
      return true;
    } catch (err: unknown) {
      let msg = 'Không thể xác định vị trí hiện tại. Bạn có thể chọn tỉnh trong danh sách.';
      if (err && typeof err === 'object' && 'code' in err) {
        const geoCode = (err as GeolocationPositionError).code;
        if (geoCode === 1) {
          msg = 'Bạn đã từ chối quyền truy cập vị trí. Hãy chọn tỉnh thủ công bên dưới.';
        } else if (geoCode === 2) {
          msg = 'Không thu được tín hiệu vị trí. Vui lòng chọn tỉnh thủ công.';
        } else if (geoCode === 3) {
          msg = 'Hết thời gian định vị GPS. Vui lòng thử lại hoặc chọn tỉnh thủ công.';
        }
      }
      setLocateFeedback({ type: 'error', text: msg });
      return false;
    } finally {
      setLocating(false);
    }
  }, []);

  const selectedRegionObj = useMemo(() => {
    if (!provinceCode || provinceCode === 'all') return null;
    return regions.find((r) => r.code === provinceCode) || null;
  }, [regions, provinceCode]);

  const provinceName = useMemo(() => {
    if (!provinceCode || provinceCode === 'all') return 'Toàn quốc';
    return selectedRegionObj?.name || provinceCode;
  }, [provinceCode, selectedRegionObj]);

  const value = useMemo(
    () => ({
      provinceCode,
      provinceName,
      selectedRegionObj,
      regions,
      loadingRegions,
      locating,
      locateFeedback,
      setProvinceCode,
      detectMyLocation,
      clearLocateFeedback,
    }),
    [
      provinceCode,
      provinceName,
      selectedRegionObj,
      regions,
      loadingRegions,
      locating,
      locateFeedback,
      setProvinceCode,
      detectMyLocation,
      clearLocateFeedback,
    ]
  );

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>;
}

export function useLocation(): LocationContextValue {
  const ctx = useContext(LocationContext);
  if (!ctx) {
    throw new Error('useLocation must be used within LocationProvider');
  }
  return ctx;
}

