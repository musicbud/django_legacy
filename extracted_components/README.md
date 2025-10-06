# Extracted Flutter Components from Commit 6cac314

This directory contains the extracted working dynamic components from commit 6cac314, integrated into the current Django backend app.

## Components Extracted

### 1. BLoCs (Business Logic Components)
- **BudMatchingBloc** (`bud_matching_bloc.dart`): Handles bud matching functionality with events for searching buds, getting profiles, liked content, top content, played tracks, and common content.
- **UserProfileBloc** (`user_profile_bloc.dart`): Manages user profile operations including fetching, updating, and managing user content.

### 2. UI Components
- **AppButton** (`app_button.dart`): Reusable button component with multiple variants (primary, secondary, text, ghost), sizes, and states (loading, disabled).
- **AppCard** (`app_card.dart`): Flexible card component with various variants (primary, secondary, outline, elevated, musicTrack, profile, event, gradient, transparent).
- **AppInputField** (`app_input_field.dart`): Comprehensive input field with multiple variants, validation, and styling options.

### 3. Pages/Screens
- **DiscoverScreen** (`discover_screen.dart`): Main discover page with search, featured artists, trending tracks, new releases, and discover more sections.
- **HomeScreen** (`home_screen.dart`): Personalized home screen with user profile integration, search, quick actions, recommendations, and recent activity.
- **ProfileScreen** (`profile_screen.dart`): User profile management screen with CRUD operations, music widgets, activity tracking, and settings.

### 4. BLoC Patterns
The extracted components demonstrate proper BLoC patterns:
- **BlocProvider**: Provides BLoC instances to widget trees
- **BlocBuilder**: Rebuilds UI based on state changes
- **BlocListener**: Handles side effects like showing snackbars or navigation

### 5. DesignSystem Integration
All components integrate with the DesignSystem theme, using:
- Semantic color tokens (primary, surface, onSurface, etc.)
- Typography scale with consistent font sizes and weights
- Spacing and radius tokens
- Gradient definitions
- Theme-aware color selection

## API Integration

The backend Django app has been updated with the following API endpoints to support these components:

### Content Endpoints
- `GET /content/tracks` - Get tracks
- `GET /content/artists` - Get artists
- `GET /content/albums` - Get albums
- `GET /content/playlists` - Get playlists
- `GET /content/genres` - Get genres

### Search Endpoints
- `GET /search` - General search
- `GET /search/suggestions` - Search suggestions
- `GET /search/recent` - Recent searches
- `GET /search/trending` - Trending searches

### Library Endpoints
- `GET /library` - Get user library
- `GET /library/playlists` - Get user playlists
- `GET /library/liked` - Get liked content
- `GET /library/downloads` - Get downloads
- `GET /library/recent` - Get recent content

### Event Endpoints
- `GET /events` - Get events
- `GET /events/<id>` - Get specific event

### Analytics Endpoints
- `GET /analytics` - Get analytics data
- `GET /analytics/stats` - Get analytics statistics

## Usage

These components are designed to work together to provide a complete music discovery and social platform experience. The BLoCs handle all business logic, the UI components provide consistent styling, and the screens integrate everything with real API calls.

## Integration Notes

- All components use the DesignSystem for theming
- BLoC pattern ensures separation of concerns
- Components are highly reusable and customizable
- API responses follow consistent pagination and error handling patterns
- Components support both light and dark themes