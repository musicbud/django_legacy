import 'package:flutter/material.dart';
import '../../../core/theme/design_system.dart';

enum AppButtonVariant {
  primary,
  secondary,
  text,
  ghost,
}

enum AppButtonSize {
  small,
  medium,
  large,
  xlarge,
}

/// Reusable Button Component based on Figma Design
class AppButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final AppButtonVariant variant;
  final AppButtonSize size;
  final IconData? icon;
  final bool isLoading;
  final bool isDisabled;
  final double? width;
  final Color? textColor;
  final Color? borderColor;
  final Color? backgroundColor;
  final bool isOutlined;

  const AppButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.variant = AppButtonVariant.primary,
    this.size = AppButtonSize.medium,
    this.icon,
    this.isLoading = false,
    this.isDisabled = false,
    this.width,
    this.textColor,
    this.borderColor,
    this.backgroundColor,
    this.isOutlined = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      height: _getHeight(),
      child: ElevatedButton(
        onPressed: (isDisabled || isLoading) ? null : onPressed,
        style: _getButtonStyle(),
        child: _buildContent(),
      ),
    );
  }

  double _getHeight() {
    switch (size) {
      case AppButtonSize.small:
        return 40;
      case AppButtonSize.medium:
        return 48;
      case AppButtonSize.large:
        return 56;
      case AppButtonSize.xlarge:
        return 64;
    }
  }

  ButtonStyle _getButtonStyle() {
    Color? buttonColor;
    Color? buttonTextColor;
    Color? buttonBorderColor;
    EdgeInsetsGeometry? padding;

    // Set colors based on variant
    switch (variant) {
      case AppButtonVariant.primary:
        buttonColor = backgroundColor ?? DesignSystem.primary;
        buttonTextColor = textColor ?? DesignSystem.onPrimary;
        buttonBorderColor = borderColor ?? DesignSystem.primary;
        break;
      case AppButtonVariant.secondary:
        buttonColor = backgroundColor ?? Colors.transparent;
        buttonTextColor = textColor ?? DesignSystem.primary;
        buttonBorderColor = borderColor ?? DesignSystem.primary;
        break;
      case AppButtonVariant.text:
        buttonColor = backgroundColor ?? Colors.transparent;
        buttonTextColor = textColor ?? DesignSystem.primary;
        buttonBorderColor = borderColor ?? Colors.transparent;
        break;
      case AppButtonVariant.ghost:
        buttonColor = backgroundColor ?? Colors.transparent;
        buttonTextColor = textColor ?? DesignSystem.onPrimary;
        buttonBorderColor = borderColor ?? DesignSystem.border;
        break;
    }

    // Set padding based on size
    switch (size) {
      case AppButtonSize.small:
        padding = EdgeInsets.symmetric(
          horizontal: DesignSystem.spacingMD,
          vertical: DesignSystem.spacingSM,
        );
        break;
      case AppButtonSize.medium:
        padding = EdgeInsets.symmetric(
          horizontal: DesignSystem.spacingLG,
          vertical: DesignSystem.spacingMD,
        );
        break;
      case AppButtonSize.large:
        padding = EdgeInsets.symmetric(
          horizontal: DesignSystem.spacingXL,
          vertical: DesignSystem.spacingLG,
        );
        break;
      case AppButtonSize.xlarge:
        padding = EdgeInsets.symmetric(
          horizontal: DesignSystem.spacingXXL,
          vertical: DesignSystem.spacingXL,
        );
        break;
    }

    return ElevatedButton.styleFrom(
      backgroundColor: isOutlined ? Colors.transparent : buttonColor,
      foregroundColor: buttonTextColor,
      side: isOutlined || buttonBorderColor != Colors.transparent
          ? BorderSide(color: buttonBorderColor!, width: 2)
          : null,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(DesignSystem.radiusMD),
      ),
      padding: padding,
      elevation: isOutlined ? 0 : (variant == AppButtonVariant.primary ? 4 : 0),
      shadowColor: isOutlined ? null : DesignSystem.primary.withValues(alpha: 0.3),
    );
  }

  Widget _buildContent() {
    if (isLoading) {
      return SizedBox(
        width: 20,
        height: 20,
        child: CircularProgressIndicator(
          strokeWidth: 2,
          valueColor: AlwaysStoppedAnimation<Color>(
            variant == AppButtonVariant.primary
                ? DesignSystem.onPrimary
                : DesignSystem.primary,
          ),
        ),
      );
    }

    final List<Widget> children = [];

    if (icon != null) {
      children.add(Icon(icon, size: _getIconSize()));
      children.add(SizedBox(width: DesignSystem.spacingSM));
    }

    children.add(Text(
      text,
      style: _getTextStyle(),
    ));

    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: children,
    );
  }

  double _getIconSize() {
    switch (size) {
      case AppButtonSize.small:
        return 16;
      case AppButtonSize.medium:
        return 20;
      case AppButtonSize.large:
        return 24;
      case AppButtonSize.xlarge:
        return 28;
    }
  }

  TextStyle _getTextStyle() {
    switch (size) {
      case AppButtonSize.small:
        return DesignSystem.titleSmall.copyWith(
          fontWeight: FontWeight.w600,
        );
      case AppButtonSize.medium:
        return DesignSystem.titleMedium.copyWith(
          fontWeight: FontWeight.w600,
        );
      case AppButtonSize.large:
        return DesignSystem.titleLarge.copyWith(
          fontWeight: FontWeight.w600,
        );
      case AppButtonSize.xlarge:
        return DesignSystem.headlineSmall.copyWith(
          fontWeight: FontWeight.w600,
        );
    }
  }

  // Helper methods for common button styles
  static AppButton primary({
    required String text,
    required VoidCallback? onPressed,
    AppButtonSize size = AppButtonSize.medium,
    IconData? icon,
    bool isLoading = false,
    double? width,
  }) {
    return AppButton(
      text: text,
      onPressed: onPressed,
      variant: AppButtonVariant.primary,
      size: size,
      icon: icon,
      isLoading: isLoading,
      width: width,
    );
  }

  static AppButton secondary({
    required String text,
    required VoidCallback? onPressed,
    AppButtonSize size = AppButtonSize.medium,
    IconData? icon,
    bool isLoading = false,
    double? width,
  }) {
    return AppButton(
      text: text,
      onPressed: onPressed,
      variant: AppButtonVariant.secondary,
      size: size,
      icon: icon,
      isLoading: isLoading,
      width: width,
    );
  }

  static AppButton ghost({
    required String text,
    required VoidCallback? onPressed,
    AppButtonSize size = AppButtonSize.medium,
    IconData? icon,
    bool isLoading = false,
    double? width,
    Color? textColor,
    Color? borderColor,
  }) {
    return AppButton(
      text: text,
      onPressed: onPressed,
      variant: AppButtonVariant.ghost,
      size: size,
      icon: icon,
      isLoading: isLoading,
      width: width,
      textColor: textColor,
      borderColor: borderColor,
    );
  }

  static AppButton tag({
    required String text,
    required VoidCallback? onPressed,
    IconData? icon,
  }) {
    return AppButton(
      text: text,
      onPressed: onPressed,
      variant: AppButtonVariant.secondary,
      size: AppButtonSize.small,
      icon: icon,
    );
  }

  static AppButton matchNow({
    required String text,
    required VoidCallback? onPressed,
    IconData? icon,
  }) {
    return AppButton(
      text: text,
      onPressed: onPressed,
      variant: AppButtonVariant.primary,
      size: AppButtonSize.large,
      icon: icon,
    );
  }
}

// Convenience class for common button patterns
class AppButtons {
  static AppButton primary({
    required String text,
    required VoidCallback? onPressed,
    AppButtonSize size = AppButtonSize.medium,
    IconData? icon,
    bool isLoading = false,
    double? width,
  }) {
    return AppButton.primary(
      text: text,
      onPressed: onPressed,
      size: size,
      icon: icon,
      isLoading: isLoading,
      width: width,
    );
  }

  static AppButton secondary({
    required String text,
    required VoidCallback? onPressed,
    AppButtonSize size = AppButtonSize.medium,
    IconData? icon,
    bool isLoading = false,
    double? width,
  }) {
    return AppButton.secondary(
      text: text,
      onPressed: onPressed,
      size: size,
      icon: icon,
      isLoading: isLoading,
      width: width,
    );
  }

  static AppButton ghost({
    required String text,
    required VoidCallback? onPressed,
    AppButtonSize size = AppButtonSize.medium,
    IconData? icon,
    bool isLoading = false,
    double? width,
    Color? textColor,
    Color? borderColor,
  }) {
    return AppButton.ghost(
      text: text,
      onPressed: onPressed,
      size: size,
      icon: icon,
      isLoading: isLoading,
      width: width,
      textColor: textColor,
      borderColor: borderColor,
    );
  }

  static AppButton tag({
    required String text,
    required VoidCallback? onPressed,
    IconData? icon,
  }) {
    return AppButton.tag(
      text: text,
      onPressed: onPressed,
      icon: icon,
    );
  }

  static AppButton matchNow({
    required String text,
    required VoidCallback? onPressed,
    IconData? icon,
  }) {
    return AppButton.matchNow(
      text: text,
      onPressed: onPressed,
      icon: icon,
    );
  }
}