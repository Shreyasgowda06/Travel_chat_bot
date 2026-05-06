---
name: Skybound Travel
colors:
  surface: '#f8f9ff'
  surface-dim: '#d0dbed'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eeff'
  surface-container-high: '#dee9fc'
  surface-container-highest: '#d9e3f6'
  on-surface: '#121c2a'
  on-surface-variant: '#3e4850'
  inverse-surface: '#27313f'
  inverse-on-surface: '#eaf1ff'
  outline: '#6e7881'
  outline-variant: '#bec8d2'
  surface-tint: '#006591'
  primary: '#006591'
  on-primary: '#ffffff'
  primary-container: '#0ea5e9'
  on-primary-container: '#003751'
  inverse-primary: '#89ceff'
  secondary: '#00668a'
  on-secondary: '#ffffff'
  secondary-container: '#40c2fd'
  on-secondary-container: '#004d6a'
  tertiary: '#8a5100'
  on-tertiary: '#ffffff'
  tertiary-container: '#de8712'
  on-tertiary-container: '#4d2b00'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c9e6ff'
  primary-fixed-dim: '#89ceff'
  on-primary-fixed: '#001e2f'
  on-primary-fixed-variant: '#004c6e'
  secondary-fixed: '#c4e7ff'
  secondary-fixed-dim: '#7bd0ff'
  on-secondary-fixed: '#001e2c'
  on-secondary-fixed-variant: '#004c69'
  tertiary-fixed: '#ffdcbd'
  tertiary-fixed-dim: '#ffb86e'
  on-tertiary-fixed: '#2c1600'
  on-tertiary-fixed-variant: '#693c00'
  background: '#f8f9ff'
  on-background: '#121c2a'
  surface-variant: '#d9e3f6'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  title-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.1px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.5px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
---

## Brand & Style

This design system establishes a high-utility, serene environment for travel planning. It merges the **clarity and deference** of Apple’s Human Interface Guidelines with the **structured logic** of Material Design 3. The brand personality is efficient yet welcoming, aiming to evoke a sense of professional reliability and lighthearted wanderlust.

The visual style is **Corporate / Modern**, leaning heavily on whitespace to reduce cognitive load during complex itinerary planning. It prioritizes content (the conversation) by using high-contrast typography and subtle depth markers to guide the user's eye without unnecessary visual noise.

## Colors

The palette is anchored by **Warm Sky Blue**, used exclusively for primary actions and user-originated content to create a clear mental model of "ownership." 

- **Primary (#0EA5E9):** Dedicated to user message bubbles and the main "Send" or "Book" actions.
- **Secondary (#38BDF8):** Used for interactive states, such as chip selection or active toggles.
- **Surface (#F9FAFB):** A light off-white that provides a softer reading experience than pure white, reducing glare during long sessions.
- **Text (#1F2937):** A deep charcoal that ensures AA/AAA accessibility compliance while appearing more sophisticated than absolute black.

## Typography

The typography utilizes **Inter** to achieve a neutral, systematic feel that scales perfectly from mobile screens to desktop. Following HIG principles, font weights are used to establish hierarchy rather than multiple typefaces. 

Headlines use tighter letter spacing for a premium editorial look, while body text and labels maintain standard tracking for maximum legibility. The system uses a strict 1.5x line-height ratio for body content to ensure the chat interface feels airy and readable.

## Layout & Spacing

The design system employs a **MD3 8dp grid system**. All margins, paddings, and component heights must be multiples of 8. 

The chatbot uses a **fluid layout** within a maximum-width container for desktop views. Message bubbles are aligned to the edges of the grid (16px margins), with a consistent 8px vertical gap between messages from the same sender and 16px between different senders. Input areas and action bars are anchored to the bottom using safe area insets to mimic native iOS behavior.

## Elevation & Depth

This design system uses **Ambient Shadows** to create a sense of verticality. Consistent with HIG's concept of depth:

1.  **Header:** Sits at the highest elevation with a fixed 8dp shadow (Blur: 16px, Y: 4px, Color: #1F2937 at 8% opacity). This ensures it remains visible as content scrolls beneath it.
2.  **Message Bubbles:** User bubbles have no shadow (flat), while system/bot bubbles feature a very soft 2dp elevation to distinguish them from the background surface.
3.  **Input Chips:** Use a tactile 1dp shadow that increases to 4dp on hover or press, providing the "squishy" physical feedback requested.
4.  **Floating Action Buttons (FAB):** Utilize a standard MD3 elevation of 6dp for high-priority transitions like "View Itinerary."

## Shapes

The shape language is defined by **High Roundedness**. 

- **Message Bubbles:** Apply a 20px corner radius. To improve conversational flow, the corner closest to the screen edge (bottom-right for user, bottom-left for bot) may be reduced to 4px to act as a "tail."
- **Chips & Inputs:** Follow a fully rounded "Pill" shape (height/2) to emphasize their interactive and tactile nature.
- **Cards:** Use a 16px (rounded-lg) radius to contain travel images and destination details, providing a friendly, approachable container.

## Components

### Buttons & Chips
- **Primary Buttons:** High-contrast Sky Blue with white text, 48px minimum height.
- **Input Chips:** Surface-colored containers with a 1px border (#E5E7EB) and a subtle 1dp shadow. Active state toggles to Sky Blue background.

### Message Bubbles
- **User Bubbles:** Sky Blue background, white text. Aligned right.
- **Bot Bubbles:** White background, Charcoal text. Aligned left. These should have a subtle 1px border to separate them from the off-white background surface.

### Input Field
- A persistent bar at the bottom of the viewport. Use a blurred backdrop effect (saturate 180%, blur 20px) behind the input container to mimic Apple's "Glassmorphism" for bottom bars.

### Travel Cards
- Used for presenting destinations. Images should have a 16px top-radius with "scrim" overlays at the bottom to ensure white text (price, location) remains legible over varying photography.

### Selection Indicators
- Checkboxes and Radios should use the Sky Blue primary color for the "Selected" state, with a standard MD3 ripple effect on tap.