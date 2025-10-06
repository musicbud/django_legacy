import 'package:flutter/material.dart';
import '../../../core/theme/design_system.dart';
import 'discover_search_section.dart';
import 'sections/featured_artists_section.dart';
import 'sections/trending_tracks_section.dart';
import 'sections/new_releases_section.dart';
import 'sections/discover_more_section.dart';

class DiscoverScreen extends StatefulWidget {
  const DiscoverScreen({super.key});

  @override
  State<DiscoverScreen> createState() => _DiscoverScreenState();
}

class _DiscoverScreenState extends State<DiscoverScreen> {
  String _selectedCategory = 'All';

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: DesignSystem.gradientBackground,
      ),
      child: CustomScrollView(
        slivers: [
          // Search and Filter Section
          SliverToBoxAdapter(
            child: DiscoverSearchSection(
              selectedCategory: _selectedCategory,
              onCategorySelected: (category) {
                setState(() {
                  _selectedCategory = category;
                });
              },
              onSearch: (query) {
                // Handle search functionality
                print('Searching for: $query');
              },
            ),
          ),

          // Featured Artists Section
          SliverToBoxAdapter(
            child: FeaturedArtistsSection(
              onViewAllPressed: () {
                // Navigate to all artists
                print('View all artists');
              },
            ),
          ),

          SliverToBoxAdapter(
            child: SizedBox(height: DesignSystem.spacingXL),
          ),

          // Trending Tracks Section
          SliverToBoxAdapter(
            child: TrendingTracksSection(
              onViewAllPressed: () {
                // Navigate to all tracks
                print('View all tracks');
              },
            ),
          ),

          SliverToBoxAdapter(
            child: SizedBox(height: DesignSystem.spacingXL),
          ),

          // New Releases Section
          SliverToBoxAdapter(
            child: NewReleasesSection(),
          ),

          SliverToBoxAdapter(
            child: SizedBox(height: DesignSystem.spacingXL),
          ),

          // Discover More Section
          SliverToBoxAdapter(
            child: DiscoverMoreSection(),
          ),

          SliverToBoxAdapter(
            child: SizedBox(height: DesignSystem.spacingXL),
          ),
        ],
      ),
    );
  }
}