'use client';

import React from 'react';
import { registerLicense } from '@syncfusion/ej2-base';
import { initSyncfusion } from '@/lib/syncfusion';

// Kích hoạt bản quyền Syncfusion v35.2.x ở top-level module scope trước khi render Grid/Chart
registerLicense(process.env.NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY || '');
initSyncfusion();

export default function SyncfusionProvider({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
