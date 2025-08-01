// Bookmark service for localStorage operations

import {
  Bookmark,
  BookmarkId,
  BookmarkStorage,
  BookmarkOperationResult,
  BookmarkFilter,
  BookmarkStats,
} from '@/types/bookmark';
import { DOMAIN_STATUS } from '@/constants/domain-status';
import { DomainResult } from '@/types/domain';

const STORAGE_KEY = 'domain-hunt-bookmarks';

// Helper function to create bookmark ID from domain and TLD
export const createBookmarkId = (domain: string, tld: string): BookmarkId => {
  const normalizedTld = tld.startsWith('.') ? tld : `.${tld}`;
  return `${domain}${normalizedTld}`;
};

// Helper function to parse domain and TLD from bookmark ID
// Note: This is a fallback method. The preferred approach is to use
// the separate domain/tld fields stored in the Bookmark object.
export const parseBookmarkId = (
  id: BookmarkId
): { domain: string; tld: string } => {
  // For proper parsing of multi-part TLD domains like example.co.uk,
  // we need to check against known multi-part TLD patterns
  const multiPartTlds = [
    '.co.uk',
    '.org.uk',
    '.ac.uk',
    '.gov.uk',
    '.net.uk',
    '.com.au',
    '.net.au',
    '.org.au',
    '.edu.au',
    '.gov.au',
    '.co.nz',
    '.net.nz',
    '.org.nz',
    '.ac.nz',
    '.govt.nz',
  ];

  // Check for multi-part TLDs first
  for (const tld of multiPartTlds) {
    if (id.endsWith(tld)) {
      const domain = id.substring(0, id.length - tld.length);
      return { domain, tld };
    }
  }

  // Fallback to simple last-dot parsing for standard TLDs
  const lastDotIndex = id.lastIndexOf('.');
  if (lastDotIndex === -1) {
    throw new Error(`Invalid bookmark ID format: ${id}`);
  }

  const domain = id.substring(0, lastDotIndex);
  const tld = id.substring(lastDotIndex);

  return { domain, tld };
};

// Load bookmarks from localStorage
const loadBookmarks = (): BookmarkStorage => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      return {
        bookmarks: [],
        lastSyncAt: new Date(),
      };
    }

    const parsed = JSON.parse(stored) as BookmarkStorage;

    // Convert date strings back to Date objects
    parsed.lastSyncAt = new Date(parsed.lastSyncAt);
    parsed.bookmarks = parsed.bookmarks.map(bookmark => ({
      ...bookmark,
      bookmarkedAt: new Date(bookmark.bookmarkedAt),
      lastCheckedAt: bookmark.lastCheckedAt
        ? new Date(bookmark.lastCheckedAt)
        : undefined,
    }));

    return parsed;
  } catch (error) {
    console.error('Failed to load bookmarks from localStorage:', error);
    return {
      bookmarks: [],
      lastSyncAt: new Date(),
    };
  }
};

// Save bookmarks to localStorage
const saveBookmarks = (storage: BookmarkStorage): void => {
  try {
    storage.lastSyncAt = new Date();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(storage));
  } catch (error) {
    console.error('Failed to save bookmarks to localStorage:', error);
  }
};

// Get all bookmarks
export const getAllBookmarks = (): Bookmark[] => {
  const storage = loadBookmarks();
  return storage.bookmarks;
};

// Get a specific bookmark by ID
export const getBookmark = (id: BookmarkId): Bookmark | null => {
  const storage = loadBookmarks();
  return storage.bookmarks.find(bookmark => bookmark.id === id) || null;
};

// Check if a domain+TLD is bookmarked
export const isBookmarked = (domain: string, tld: string): boolean => {
  const id = createBookmarkId(domain, tld);
  return getBookmark(id) !== null;
};

// Dispatch custom event when bookmarks change
const dispatchBookmarkChangeEvent = () => {
  if (typeof window !== 'undefined') {
    // Dispatch custom event for same-page components
    window.dispatchEvent(new CustomEvent('bookmarkStatsChanged'));

    // Trigger storage event for cross-tab communication
    // We temporarily set and remove a flag to trigger storage event
    const timestamp = Date.now().toString();
    localStorage.setItem('bookmarkChangeSignal', timestamp);
    // Remove immediately to avoid storage bloat
    setTimeout(() => {
      localStorage.removeItem('bookmarkChangeSignal');
    }, 100);
  }
};

// Add a bookmark
export const addBookmark = (
  domain: string,
  tld: string,
  status?: DomainResult['status']
): BookmarkOperationResult => {
  try {
    const id = createBookmarkId(domain, tld);
    const storage = loadBookmarks();

    // Check if already bookmarked
    if (storage.bookmarks.some(bookmark => bookmark.id === id)) {
      return {
        success: false,
        error: 'Domain is already bookmarked',
      };
    }

    const bookmark: Bookmark = {
      id,
      domain,
      tld,
      bookmarkedAt: new Date(),
      lastKnownStatus: status,
      lastCheckedAt: status ? new Date() : undefined,
    };

    storage.bookmarks.push(bookmark);
    saveBookmarks(storage);
    dispatchBookmarkChangeEvent();

    return {
      success: true,
      bookmark,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

// Remove a bookmark
export const removeBookmark = (
  domain: string,
  tld: string
): BookmarkOperationResult => {
  try {
    const id = createBookmarkId(domain, tld);
    const storage = loadBookmarks();

    const index = storage.bookmarks.findIndex(bookmark => bookmark.id === id);
    if (index === -1) {
      return {
        success: false,
        error: 'Bookmark not found',
      };
    }

    const removedBookmark = storage.bookmarks[index];
    storage.bookmarks.splice(index, 1);
    saveBookmarks(storage);
    dispatchBookmarkChangeEvent();

    return {
      success: true,
      bookmark: removedBookmark,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

// Toggle bookmark (add if not exists, remove if exists)
export const toggleBookmark = (
  domain: string,
  tld: string,
  status?: DomainResult['status']
): BookmarkOperationResult => {
  if (isBookmarked(domain, tld)) {
    return removeBookmark(domain, tld);
  } else {
    return addBookmark(domain, tld, status);
  }
};

// Update bookmark status (when re-checking domains)
export const updateBookmarkStatus = (
  domain: string,
  tld: string,
  status: DomainResult['status']
): BookmarkOperationResult => {
  try {
    const id = createBookmarkId(domain, tld);
    const storage = loadBookmarks();

    const bookmark = storage.bookmarks.find(b => b.id === id);
    if (!bookmark) {
      return {
        success: false,
        error: 'Bookmark not found',
      };
    }

    bookmark.lastKnownStatus = status;
    bookmark.lastCheckedAt = new Date();
    saveBookmarks(storage);
    dispatchBookmarkChangeEvent();

    return {
      success: true,
      bookmark,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

// Filter bookmarks
export const filterBookmarks = (filter: BookmarkFilter): Bookmark[] => {
  let bookmarks = getAllBookmarks();

  // Filter by status
  if (filter.status) {
    bookmarks = bookmarks.filter(
      bookmark => bookmark.lastKnownStatus === filter.status
    );
  }

  // Filter by tags
  if (filter.tags && filter.tags.length > 0) {
    bookmarks = bookmarks.filter(
      bookmark =>
        bookmark.tags && bookmark.tags.some(tag => filter.tags!.includes(tag))
    );
  }

  // Filter by search term
  if (filter.searchTerm) {
    const searchLower = filter.searchTerm.toLowerCase();
    bookmarks = bookmarks.filter(
      bookmark =>
        bookmark.domain.toLowerCase().includes(searchLower) ||
        bookmark.tld.toLowerCase().includes(searchLower) ||
        bookmark.notes?.toLowerCase().includes(searchLower)
    );
  }

  // Sort bookmarks
  const sortBy = filter.sortBy || 'bookmarkedAt';
  const sortOrder = filter.sortOrder || 'desc';

  bookmarks.sort((a, b) => {
    let aValue: string | Date, bValue: string | Date;

    switch (sortBy) {
      case 'domain':
        aValue = a.domain;
        bValue = b.domain;
        break;
      case 'lastCheckedAt':
        aValue = a.lastCheckedAt || new Date(0);
        bValue = b.lastCheckedAt || new Date(0);
        break;
      case 'bookmarkedAt':
      default:
        aValue = a.bookmarkedAt;
        bValue = b.bookmarkedAt;
        break;
    }

    if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  return bookmarks;
};

// Get bookmark statistics
export const getBookmarkStats = (): BookmarkStats => {
  const bookmarks = getAllBookmarks();

  return {
    total: bookmarks.length,
    available: bookmarks.filter(
      b => b.lastKnownStatus === DOMAIN_STATUS.AVAILABLE
    ).length,
    taken: bookmarks.filter(b => b.lastKnownStatus === DOMAIN_STATUS.TAKEN)
      .length,
    errors: bookmarks.filter(
      b => !b.lastKnownStatus || b.lastKnownStatus === DOMAIN_STATUS.ERROR
    ).length,
  };
};

// Clear all bookmarks (for debugging/reset)
export const clearAllBookmarks = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error('Failed to clear bookmarks:', error);
  }
};
