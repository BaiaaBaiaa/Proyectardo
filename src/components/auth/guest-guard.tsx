'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from '@/hooks/use-user';

export function GuestGuard({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useUser();
  const router = useRouter();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    if (!isLoading) {
      if (user?.token) {
        router.push('/dashboard');
      } else {
        setChecked(true);
      }
    }
  }, [user, isLoading, router]);

  if (!checked && !isLoading) return null;

  return <>{children}</>;
}
