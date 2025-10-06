import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../blocs/user_profile/user_profile_bloc.dart';
import '../../../core/theme/design_system.dart';
import '../../widgets/common/index.dart';
import 'profile_header_widget.dart';
import 'profile_music_widget.dart';
import 'profile_activity_widget.dart';
import 'profile_settings_widget.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  void initState() {
    super.initState();
    // Load user profile when page initializes
    context.read<UserProfileBloc>().add(FetchMyProfile());
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<UserProfileBloc, UserProfileState>(
      listener: (context, state) {
        if (state is UserProfileError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error: ${state.message}'),
              backgroundColor: DesignSystem.error,
            ),
          );
        } else if (state is UserProfileUpdated) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Text('Profile updated successfully'),
              backgroundColor: DesignSystem.success,
            ),
          );
          // Refresh profile after update
          context.read<UserProfileBloc>().add(FetchMyProfile());
        }
      },
      child: BlocBuilder<UserProfileBloc, UserProfileState>(
        builder: (context, state) {
          return Container(
            decoration: BoxDecoration(
              gradient: DesignSystem.gradientBackground,
            ),
            child: CustomScrollView(
              slivers: [
                // Profile Header Section
                SliverToBoxAdapter(
                  child: ProfileHeaderWidget(
                    userProfile: state is UserProfileLoaded ? state.userProfile : null,
                    isLoading: state is UserProfileLoading,
                    hasError: state is UserProfileError,
                  ),
                ),

                // Profile Sections
                if (state is UserProfileLoaded) ...[
                  SliverToBoxAdapter(child: SizedBox(height: DesignSystem.spacingXL)),

                  // My Music Section
                  SliverToBoxAdapter(
                    child: ProfileMusicWidget(),
                  ),

                  SliverToBoxAdapter(child: SizedBox(height: DesignSystem.spacingXL)),

                  // Recent Activity Section
                  SliverToBoxAdapter(
                    child: ProfileActivityWidget(),
                  ),

                  SliverToBoxAdapter(child: SizedBox(height: DesignSystem.spacingXL)),

                  // Settings Section
                  SliverToBoxAdapter(
                    child: ProfileSettingsWidget(),
                  ),

                  SliverToBoxAdapter(child: SizedBox(height: DesignSystem.spacingXL)),

                  // Logout Section
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: DesignSystem.spacingLG),
                      child: OutlineButton(
                        text: 'Logout',
                        onPressed: () {
                          // Handle logout
                        },
                        icon: Icons.logout,
                        size: ModernButtonSize.large,
                        isFullWidth: true,
                      ),
                    ),
                  ),

                  SliverToBoxAdapter(child: SizedBox(height: DesignSystem.spacingXL)),
                ],
              ],
            ),
          );
        },
      ),
    );
  }
}