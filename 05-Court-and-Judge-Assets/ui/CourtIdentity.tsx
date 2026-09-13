import { useEffect, useState } from 'react';
import './court-identity.css';

export interface CourtAssetMapping {
  court_id: string;
  name: string;
  homepage: string;
  fallback_text: string;
  primary_asset_path: string | null;
  primary_background: string;
  compact_asset_path: string | null;
  compact_background: string;
}

interface Props {
  court: CourtAssetMapping;
  assetBaseUrl: string;
  variant?: 'compact' | 'wordmark';
  showName?: boolean;
}

/** Presentational adapter only. The host supplies canonical court identity data. */
export function CourtIdentity({ court, assetBaseUrl, variant = 'compact', showName = false }: Props) {
  const path = variant === 'compact' ? court.compact_asset_path : court.primary_asset_path;
  const background = variant === 'compact' ? court.compact_background : court.primary_background;
  const [failedPath, setFailedPath] = useState<string | null>(null);
  useEffect(() => { setFailedPath(null); }, [court.court_id, path]);
  // Only local content-addressed images from this pack are accepted as relative paths.
  const validPath = path && /^images\/[a-f0-9]{2}\/[a-f0-9]{64}\.(png|jpe?g|gif|webp|svg|ico|bmp|tif)$/.test(path);
  const imageUrl = validPath && failedPath !== path ? `${assetBaseUrl.replace(/\/$/, '')}/${path}` : null;
  return (
    <span className="court-identity">
      <span className={`court-identity__image court-identity__image--${variant}${imageUrl && background === 'dark' ? ' court-identity__image--dark' : ''}`}>
        {imageUrl ? (
          <img src={imageUrl} alt={showName ? '' : court.name} loading="lazy" decoding="async" onError={() => setFailedPath(path)} />
        ) : (
          <span className="court-identity__fallback" role="img" aria-label={showName ? undefined : court.name} aria-hidden={showName || undefined}>{court.fallback_text}</span>
        )}
      </span>
      {showName && <span className="court-identity__name">{court.name}</span>}
    </span>
  );
}
