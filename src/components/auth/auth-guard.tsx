'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from '@/hooks/use-user';

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user?.token) {
      router.push('/auth/sign-in');
    }
  }, [user, isLoading, router]);

  if (isLoading || !user?.token) return null;

  return <>{children}</>;
}
