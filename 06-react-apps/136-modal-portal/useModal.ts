'use client';

import { useState, useCallback, useEffect } from 'react';

/**
 * useModal Hook
 *
 * A hook to manage modal open/close state with programmatic control.
 * Provides open, close, and toggle functions.
 */

interface UseModalOptions {
  onOpen?: () => void;
  onClose?: () => void;
  defaultOpen?: boolean;
}

interface UseModalReturn {
  isOpen: boolean;
  open: () => void;
  close: () => void;
  toggle: () => void;
}

export function useModal(options: UseModalOptions = {}): UseModalReturn {
  const { onOpen, onClose, defaultOpen = false } = options;
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const open = useCallback(() => {
    setIsOpen(true);
    onOpen?.();
  }, [onOpen]);

  const close = useCallback(() => {
    setIsOpen(false);
    onClose?.();
  }, [onClose]);

  const toggle = useCallback(() => {
    if (isOpen) {
      close();
    } else {
      open();
    }
  }, [isOpen, open, close]);

  return { isOpen, open, close, toggle };
}

/**
 * useModalGroup Hook
 *
 * Manages multiple modals with unique keys.
 */

interface UseModalGroupOptions {
  onOpen?: (key: string) => void;
  onClose?: (key: string) => void;
}

type ModalKey = string | number;

interface UseModalGroupReturn<K extends ModalKey> {
  isOpen: (key: K) => boolean;
  open: (key: K) => void;
  close: (key: K) => void;
  closeAll: () => void;
  activeModal: K | null;
}

export function useModalGroup<K extends ModalKey>(
  options: UseModalGroupOptions = {}
): UseModalGroupReturn<K> {
  const { onOpen, onClose } = options;
  const [openModals, setOpenModals] = useState<Set<K>>(new Set());

  const isOpen = useCallback((key: K) => openModals.has(key), [openModals]);

  const open = useCallback((key: K) => {
    setOpenModals((prev) => new Set([...prev, key]));
    onOpen?.(key);
  }, [onOpen]);

  const close = useCallback((key: K) => {
    setOpenModals((prev) => {
      const next = new Set(prev);
      next.delete(key);
      return next;
    });
    onClose?.(key);
  }, [onClose]);

  const closeAll = useCallback(() => {
    setOpenModals(new Set());
  }, []);

  // Get the most recently opened modal
  const activeModal = openModals.size > 0
    ? Array.from(openModals).pop() ?? null
    : null;

  return { isOpen, open, close, closeAll, activeModal };
}

/**
 * useFocusTrap Hook
 *
 * Traps focus within a container element.
 */

interface UseFocusTrapOptions {
  enabled?: boolean;
  onEscape?: () => void;
}

export function useFocusTrap(
  containerRef: React.RefObject<HTMLElement>,
  options: UseFocusTrapOptions = {}
) {
  const { enabled = true, onEscape } = options;

  useEffect(() => {
    if (!enabled) return;

    const FOCUSABLE_SELECTOR = [
      'a[href]',
      'button:not([disabled])',
      'textarea:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      '[tabindex]:not([tabindex="-1"])',
    ].join(', ');

    const container = containerRef.current;
    if (!container) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && onEscape) {
        onEscape();
        return;
      }

      if (e.key !== 'Tab') return;

      const focusable = Array.from(
        container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)
      );

      if (focusable.length === 0) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      const active = document.activeElement;

      if (e.shiftKey) {
        if (active === first || !container.contains(active)) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (active === last || !container.contains(active)) {
          e.preventDefault();
          first.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [enabled, containerRef, onEscape]);
}

/**
 * useScrollLock Hook
 *
 * Locks body scroll when active.
 */

export function useScrollLock(enabled: boolean = true) {
  useEffect(() => {
    if (!enabled) return;

    const originalOverflow = document.body.style.overflow;
    const originalPaddingRight = document.body.style.paddingRight;

    // Calculate scrollbar width
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;

    document.body.style.overflow = 'hidden';
    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }

    return () => {
      document.body.style.overflow = originalOverflow;
      document.body.style.paddingRight = originalPaddingRight;
    };
  }, [enabled]);
}

export default useModal;
