import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../blocs/user_profile/user_profile_bloc.dart';
import '../../../core/theme/design_system.dart';
import '../../widgets/common/index.dart';
import '../../widgets/navigation/main_navigation_scaffold.dart';
import '../../navigation/main_navigation.dart';
import 'home_header_widget.dart';
import 'home_quick_actions.dart';
import 'home_recommendations.dart';
import 'home_recent_activity.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _searchController = TextEditingController();
  late final MainNavigationController _navigationController;

  @override
  void initState() {
    super.initState();
    _navigationController = MainNavigationController();

    // Load user profile and dynamic content
    context.read<UserProfileBloc>().add(FetchMyProfile());
    context.read<UserProfileBloc>().add(FetchMyLikedContent(contentType: 'tracks'));
    context.read<UserProfileBloc>().add(FetchMyTopContent(contentType: 'artists'));
    context.read<UserProfileBloc>().add(FetchMyPlayedTracks());
  }

  @override
  void dispose() {
    _searchController.dispose();
    _navigationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MainNavigationScaffold(
      navigationController: _navigationController,
      body: BlocListener<UserProfileBloc, UserProfileState>(
        listener: (context, state) {
          if (state is UserProfileError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Error: ${state.message}'),
                backgroundColor: DesignSystem.error,
              ),
            );
          }
        },
        child: Container(
          decoration: BoxDecoration(
            gradient: DesignSystem.gradientBackground,
          ),
          child: SafeArea(
            child: CustomScrollView(
              slivers: [
                // Header Section
                SliverToBoxAdapter(
                  child: HomeHeaderWidget(),
                ),

                // Search Section
                SliverToBoxAdapter(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: DesignSystem.spacingLG),
                    child: ModernInputField(
                      hintText: 'Search for music, artists, or playlists...',
                      controller: _searchController,
                      onChanged: (value) {
                        if (value.isNotEmpty) {
                          // Navigate to search page with query
                          Navigator.pushNamed(
                            context,
                            '/search',
                            arguments: {'query': value},
                          );
                        }
                      },
                      size: ModernInputFieldSize.large,
                    ),
                  ),
                ),

                SliverToBoxAdapter(
                  child: SizedBox(height: DesignSystem.spacingLG),
                ),

                // Quick Actions Section
                SliverToBoxAdapter(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: DesignSystem.spacingLG),
                    child: HomeQuickActions(),
                  ),
                ),

                SliverToBoxAdapter(
                  child: SizedBox(height: DesignSystem.spacingXL),
                ),

                // Dynamic Content Sections
                SliverToBoxAdapter(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: DesignSystem.spacingLG),
                    child: Column(
                      children: [
                        HomeRecommendations(),
                        HomeRecentActivity(),
                      ],
                    ),
                  ),
                ),

                SliverToBoxAdapter(
                  child: SizedBox(height: DesignSystem.spacingXL),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}