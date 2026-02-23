# Copyright 2025 Adobe. All rights reserved.

"""
Helper script for shaping fonts with HarfBuzz.
Used as part of the integration tests for variable fonts.
Provides a stable interface for font shaping operations that can
adapt if the underlying uharfbuzz API changes.
"""

import argparse
import json
import logging
import os
import sys
from typing import Dict, List, Optional, Tuple, Union

try:
    import uharfbuzz as hb
except ImportError:
    hb = None

__version__ = '0.1.0'

logger = logging.getLogger('shaper')


class ShapingResult:
    """
    Encapsulates the results of shaping a text string.
    """
    def __init__(self, text: str, glyphs: List[int],
                 advances: List[int], positions: List[Tuple[int, int]],
                 location: Optional[Dict[str, float]] = None):
        self.text = text
        self.glyphs = glyphs  # List of glyph IDs
        self.advances = advances  # List of x-advance values
        self.positions = positions  # List of (x_offset, y_offset) tuples
        self.location = location or {}

    def __repr__(self):
        loc_str = ', '.join(f"{k}={v}" for k, v in self.location.items())
        return (f"ShapingResult(text={self.text!r}, location=[{loc_str}], "
                f"glyphs={self.glyphs}, advances={self.advances})")

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'text': self.text,
            'glyphs': self.glyphs,
            'advances': self.advances,
            'positions': self.positions,
            'location': self.location
        }


class Shaper:
    """
    Handles font loading and shaping operations with HarfBuzz.
    """

    def __init__(self, font_path: str, features: Optional[List[str]] = None):
        """
        Initialize the shaper with a font file.

        Args:
            font_path: Path to the font file
            features: Optional list of feature tags to enable (e.g., ['kern', 'liga'])
        """
        if hb is None:
            raise ImportError("uharfbuzz is not installed. "
                            "Install with: pip install uharfbuzz")

        self.font_path = font_path
        self.features = features or []

        # Load font
        self.blob = hb.Blob.from_file_path(font_path)
        self.face = hb.Face(self.blob)
        self.font = hb.Font(self.face)

        # Cache axis information
        self._axis_info = None

    @property
    def axis_info(self) -> List[Dict[str, Union[str, float]]]:
        """Get information about variable font axes."""
        if self._axis_info is None:
            self._axis_info = []
            # Check if this is a variable font
            if hasattr(self.face, 'has_var_data') and self.face.has_var_data():
                # Note: uharfbuzz 0.45.0 doesn't expose axis info directly
                # We'll add this when needed or upgrade uharfbuzz
                logger.debug("Variable font detected")
        return self._axis_info

    def shape(self, text: str, location: Optional[Dict[str, float]] = None,
              features: Optional[List[str]] = None) -> ShapingResult:
        """
        Shape a text string at a specific design space location.

        Args:
            text: Text to shape
            location: Design space location as {axis_tag: value}
            features: Optional list of features for this shaping only

        Returns:
            ShapingResult object with glyphs, advances, and positions
        """
        # Set variation coordinates if provided
        if location:
            self._set_variations(location)

        # Create buffer and shape
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()

        # Build features dict for shaping
        feature_list = features or self.features
        if feature_list:
            # Convert feature list to dict of {tag: True}
            features_dict = {tag: True for tag in feature_list}
            hb.shape(self.font, buf, features=features_dict)
        else:
            hb.shape(self.font, buf)

        # Extract results
        infos = buf.glyph_infos
        positions = buf.glyph_positions

        glyphs = [info.codepoint for info in infos]
        advances = [pos.x_advance for pos in positions]
        offsets = [(pos.x_offset, pos.y_offset) for pos in positions]

        return ShapingResult(text, glyphs, advances, offsets, location)

    def _set_variations(self, location: Dict[str, float]):
        """Set variation coordinates for variable fonts."""
        try:
            self.font.set_variations(location)
            logger.debug(f"Set variation coordinates: {location}")
        except Exception as e:
            logger.warning(f"Failed to set variations {location}: {e}")

    def get_advance_width(self, text: str, location: Optional[Dict[str, float]] = None) -> int:
        """
        Get the total advance width of shaped text.

        Args:
            text: Text to shape
            location: Optional design space location

        Returns:
            Total advance width in font units
        """
        result = self.shape(text, location)
        return sum(result.advances)


def compare_values(expected: Union[int, float],
                   actual: Union[int, float],
                   tolerance: Union[int, float] = 0) -> bool:
    """
    Compare two numeric values with tolerance.

    Args:
        expected: Expected value
        actual: Actual value
        tolerance: Allowed difference (absolute)

    Returns:
        True if values match within tolerance
    """
    return abs(expected - actual) <= tolerance


def compare_results(result1: ShapingResult,
                   result2: ShapingResult,
                   tolerance: int = 0,
                   check_glyphs: bool = True,
                   check_advances: bool = True,
                   check_positions: bool = False) -> Tuple[bool, List[str]]:
    """
    Compare two shaping results.

    Args:
        result1: First result
        result2: Second result
        tolerance: Tolerance for numeric comparisons
        check_glyphs: Whether to compare glyph IDs
        check_advances: Whether to compare advances
        check_positions: Whether to compare positions

    Returns:
        Tuple of (success: bool, differences: List[str])
    """
    differences = []

    if check_glyphs and result1.glyphs != result2.glyphs:
        differences.append(
            f"Glyphs differ: {result1.glyphs} != {result2.glyphs}")

    if check_advances:
        if len(result1.advances) != len(result2.advances):
            differences.append(
                f"Advance count differs: {len(result1.advances)} != {len(result2.advances)}")
        else:
            for i, (adv1, adv2) in enumerate(zip(result1.advances, result2.advances)):
                if not compare_values(adv1, adv2, tolerance):
                    differences.append(
                        f"Advance {i} differs: {adv1} != {adv2} (tolerance={tolerance})")

    if check_positions:
        if len(result1.positions) != len(result2.positions):
            differences.append(
                f"Position count differs: {len(result1.positions)} != {len(result2.positions)}")
        else:
            for i, (pos1, pos2) in enumerate(zip(result1.positions, result2.positions)):
                if not (compare_values(pos1[0], pos2[0], tolerance) and
                       compare_values(pos1[1], pos2[1], tolerance)):
                    differences.append(
                        f"Position {i} differs: {pos1} != {pos2} (tolerance={tolerance})")

    return (len(differences) == 0, differences)


def get_options(args=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version',
        action='version',
        version=__version__
    )
    parser.add_argument(
        'font_path',
        type=_validate_path,
        help='Path to font file'
    )
    parser.add_argument(
        '-t', '--text',
        required=True,
        help='Text to shape'
    )
    parser.add_argument(
        '-l', '--location',
        help='Design space location as JSON, e.g., \'{"wght": 700, "opsz": 20}\''
    )
    parser.add_argument(
        '-f', '--features',
        help='Comma-separated list of OpenType features to enable'
    )
    parser.add_argument(
        '-o', '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    return parser.parse_args(args)


def _validate_path(path_str):
    """Validate that a path exists."""
    valid_path = os.path.abspath(os.path.realpath(path_str))
    if not os.path.exists(valid_path):
        raise argparse.ArgumentTypeError(
            f"'{path_str}' is not a valid path.")
    return valid_path


def main(args=None):
    """
    Main entry point for command-line usage.
    Returns 0 on success, 1 on failure.
    """
    opts = get_options(args)

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if opts.verbose else logging.INFO,
        format='%(levelname)s: %(message)s'
    )

    try:
        # Parse location if provided
        location = None
        if opts.location:
            location = json.loads(opts.location)

        # Parse features if provided
        features = None
        if opts.features:
            features = [f.strip() for f in opts.features.split(',')]

        # Create shaper and shape text
        shaper = Shaper(opts.font_path, features=features)
        result = shaper.shape(opts.text, location=location)

        # Output results
        if opts.output == 'json':
            print(json.dumps(result.to_dict(), indent=2))
        else:  # text
            print(f"Text: {result.text}")
            if result.location:
                loc_str = ', '.join(f"{k}={v}" for k, v in result.location.items())
                print(f"Location: {loc_str}")
            print(f"Glyphs: {result.glyphs}")
            print(f"Advances: {result.advances}")
            print(f"Total advance: {sum(result.advances)}")
            if any(pos != (0, 0) for pos in result.positions):
                print(f"Positions: {result.positions}")

        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        if opts.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
