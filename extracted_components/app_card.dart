import 'package:flutter/material.dart';
import '../../../core/theme/design_system.dart';

enum AppCardVariant {
  primary,
  secondary,
  outline,
  elevated,
  musicTrack,
  profile,
  event,
  gradient,
  transparent,
}

class AppCard extends StatelessWidget {
  final AppCardVariant variant;
  final Widget? child;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final VoidCallback? onTap;
  final double? width;
  final double? height;
  final BorderRadius? borderRadius;
  final BoxShadow? shadow;

  const AppCard({
    super.key,
    this.variant = AppCardVariant.primary,
    this.child,
    this.padding,
    this.margin,
    this.onTap,
    this.width,
    this.height,
    this.borderRadius,
    this.shadow,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: width,
        height: height,
        margin: margin,
        padding: padding ?? EdgeInsets.all(DesignSystem.spacingMD),
        decoration: _getDecoration(),
        child: child,
      ),
    );
  }

  BoxDecoration _getDecoration() {
    switch (variant) {
      case AppCardVariant.primary:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          border: Border.all(
            color: DesignSystem.border.withValues(alpha: 0.2),
          ),
        );
      case AppCardVariant.secondary:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          border: Border.all(
            color: DesignSystem.primary.withValues(alpha: 0.3),
          ),
        );
      case AppCardVariant.outline:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          border: Border.all(
            color: DesignSystem.border.withValues(alpha: 0.3),
          ),
        );
      case AppCardVariant.elevated:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          boxShadow: DesignSystem.shadowMedium,
        );
      case AppCardVariant.musicTrack:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          border: Border.all(
            color: DesignSystem.border.withValues(alpha: 0.2),
          ),
        );
      case AppCardVariant.profile:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          border: Border.all(
            color: DesignSystem.border.withValues(alpha: 0.2),
          ),
        );
      case AppCardVariant.event:
        return BoxDecoration(
          color: DesignSystem.surfaceContainer,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
          border: Border.all(
            color: DesignSystem.border.withValues(alpha: 0.2),
          ),
        );
      case AppCardVariant.gradient:
        return BoxDecoration(
          gradient: DesignSystem.gradientPrimary,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
        );
      case AppCardVariant.transparent:
        return BoxDecoration(
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLG),
        );
    }
  }
}

// Factory constructors for common card types
class AppCards {
  static AppCard musicTrack({
    Key? key,
    required String title,
    required String artist,
    required String album,
    required String imageUrl,
    required String duration,
    bool isLiked = false,
    VoidCallback? onTap,
    VoidCallback? onLike,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.musicTrack,
      onTap: onTap,
      child: Row(
        children: [
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              image: DecorationImage(
                image: NetworkImage(imageUrl),
                fit: BoxFit.cover,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '$artist • $album',
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          IconButton(
            icon: Icon(
              isLiked ? Icons.favorite : Icons.favorite_border,
              color: isLiked ? Colors.red : Colors.grey,
            ),
            onPressed: onLike,
          ),
        ],
      ),
    );
  }

  static AppCard profile({
    Key? key,
    required String name,
    required String role,
    required String imageUrl,
    bool isOnline = false,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.profile,
      onTap: onTap,
      child: Row(
        children: [
          Stack(
            children: [
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(25),
                  image: DecorationImage(
                    image: NetworkImage(imageUrl),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              if (isOnline)
                Positioned(
                  right: 0,
                  bottom: 0,
                  child: Container(
                    width: 16,
                    height: 16,
                    decoration: BoxDecoration(
                      color: Colors.green,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.white, width: 2),
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  role,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  static AppCard event({
    Key? key,
    required String title,
    required String subtitle,
    required String date,
    required String location,
    required String imageUrl,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.event,
      onTap: onTap,
      child: Row(
        children: [
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              image: DecorationImage(
                image: NetworkImage(imageUrl),
                fit: BoxFit.cover,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  date,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 12,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  location,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  static AppCard gradient({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.gradient,
      onTap: onTap,
      child: child,
    );
  }

  static AppCard defaultCard({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.primary,
      onTap: onTap,
      child: child,
    );
  }

  static AppCard white({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.primary,
      onTap: onTap,
      child: child,
    );
  }

  static AppCard transparent({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.transparent,
      onTap: onTap,
      child: child,
    );
  }

  static AppCard glass({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.transparent,
      onTap: onTap,
      child: child,
    );
  }

  static AppCard outlined({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.outline,
      onTap: onTap,
      child: child,
    );
  }

  static AppCard bordered({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
  }) {
    return AppCard(
      key: key,
      variant: AppCardVariant.outline,
      onTap: onTap,
      child: child,
    );
  }
}