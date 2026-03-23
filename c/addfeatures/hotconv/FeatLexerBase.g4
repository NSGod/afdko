/* Copyright 2021,2024 Adobe Systems Incorporated (http://www.adobe.com/). All Rights Reserved.
 * This software is licensed as OpenSource, under the Apache License, Version 2.0.
 * This license is available at: http://opensource.org/licenses/Apache-2.0.
 */

// -------------------------- Feature file tokens ---------------------------

lexer grammar FeatLexerBase;

// Declare token types used in modes
tokens { AXISUNIT }

COMMENT                 : '#' ~[\r\n]* -> skip ;
WHITESPACE              : [ \t\r\n]+ -> skip ;

INCLUDE                 : 'include' -> pushMode(Include) ;
FEATURE                 : 'feature' ;
TABLE                   : 'table' ;
SCRIPT                  : 'script' ;
LANGUAGE                : 'language' ;
LANGSYS                 : 'languagesystem' ;
SUBTABLE                : 'subtable';
LOOKUP                  : 'lookup' ;
LOOKUPFLAG              : 'lookupflag' ;
NOTDEF                  : '.notdef' ;

RIGHT_TO_LEFT           : 'RightToLeft' ;
IGNORE_BASE_GLYPHS      : 'IgnoreBaseGlyphs' ;
IGNORE_LIGATURES        : 'IgnoreLigatures' ;
IGNORE_MARKS            : 'IgnoreMarks' ;
USE_MARK_FILTERING_SET  : 'UseMarkFilteringSet' ;
MARK_ATTACHMENT_TYPE    : 'MarkAttachmentType' ;

ANON                    : 'anon' ;
ANON_v                  : 'anonymous' ;

EXCLUDE_DFLT            : 'excludeDFLT' ;
INCLUDE_DFLT            : 'includeDFLT' ;
EXCLUDE_dflt            : 'exclude_dflt' ;
INCLUDE_dflt            : 'include_dflt' ;

USE_EXTENSION           : 'useExtension' ;
BEGINVALUE              : '<' ;
ENDVALUE                : '>' ;
ENUMERATE               : 'enumerate' ;
ENUMERATE_v             : 'enum' ;
EXCEPT                  : 'except' ;
IGNORE                  : 'ignore' ;
SUBSTITUTE              : 'substitute' ;
SUBSTITUTE_v            : 'sub' ;
REVERSE                 : 'reversesub' ;
REVERSE_v               : 'rsub' ;
BY                      : 'by' ;
FROM                    : 'from' ;
POSITION                : 'position' ;
POSITION_v              : 'pos';
PARAMETERS              : 'parameters' ;
FEATURE_NAMES           : 'featureNames' ;
CV_PARAMETERS           : 'cvParameters' ;
CV_UI_LABEL             : 'FeatUILabelNameID' ;
CV_TOOLTIP              : 'FeatUITooltipTextNameID' ;
CV_SAMPLE_TEXT          : 'SampleTextNameID' ;
CV_PARAM_LABEL          : 'ParamUILabelNameID' ;
CV_CHARACTER            : 'Character' ;
SIZEMENUNAME            : 'sizemenuname' ;
CONTOURPOINT            : 'contourpoint' ;
ANCHOR                  : 'anchor' ;
ANCHOR_DEF              : 'anchorDef' ;
VALUE_RECORD_DEF        : 'valueRecordDef' ;
LOCATION_DEF            : 'locationDef' -> pushMode(LocationDefMode) ;
MARK                    : 'mark';
MARK_CLASS              : 'markClass' ;
CURSIVE                 : 'cursive' ;
MARKBASE                : 'base' ;
MARKLIG                 : 'ligature' ;
MARKLIG_v               : 'lig' ;
LIG_COMPONENT           : 'ligComponent' ;

KNULL                   : 'NULL' ;

BASE                    : 'BASE' ;
HA_BTL                  : 'HorizAxis.BaseTagList' ;
VA_BTL                  : 'VertAxis.BaseTagList' ;
HA_BSL                  : 'HorizAxis.BaseScriptList' ;
VA_BSL                  : 'VertAxis.BaseScriptList' ;

GDEF                    : 'GDEF' ;
GLYPH_CLASS_DEF         : 'GlyphClassDef' ;
ATTACH                  : 'Attach' ;
LIG_CARET_BY_POS        : 'LigatureCaretByPos' ;
LIG_CARET_BY_IDX        : 'LigatureCaretByIndex' ;

HEAD                    : 'head' ;
FONT_REVISION           : 'FontRevision' ;

HHEA                    : 'hhea' ;
ASCENDER                : 'Ascender' ;
DESCENDER               : 'Descender' ;
LINE_GAP                : 'LineGap' ;

CARET_OFFSET            : 'CaretOffset' ;
CARET_SLOPE_RISE        : 'CaretSlopeRise' ;
CARET_SLOPE_RUN         : 'CaretSlopeRun' ;

NAME                    : 'name' ;
NAMEID                  : 'nameid' ;

OS_2                    : 'OS/2' ;
FS_TYPE                 : 'FSType' ;
FS_TYPE_v               : 'fsType' ;
OS2_LOWER_OP_SIZE       : 'LowerOpSize' ;
OS2_UPPER_OP_SIZE       : 'UpperOpSize' ;
PANOSE                  : 'Panose' ;
TYPO_ASCENDER           : 'TypoAscender' ;
TYPO_DESCENDER          : 'TypoDescender' ;
TYPO_LINE_GAP           : 'TypoLineGap' ;
WIN_ASCENT              : 'winAscent' ;
WIN_DESCENT             : 'winDescent' ;
X_HEIGHT                : 'XHeight' ;
CAP_HEIGHT              : 'CapHeight' ;
SUBSCRIPT_X_SIZE        : 'SubscriptXSize' ;
SUBSCRIPT_X_OFFSET      : 'SubscriptXOffset' ;
SUBSCRIPT_Y_SIZE        : 'SubscriptYSize' ;
SUBSCRIPT_Y_OFFSET      : 'SubscriptYOffset' ;
SUPERSCRIPT_X_SIZE      : 'SuperscriptXSize' ;
SUPERSCRIPT_X_OFFSET    : 'SuperscriptXOffset' ;
SUPERSCRIPT_Y_SIZE      : 'SuperscriptYSize' ;
SUPERSCRIPT_Y_OFFSET    : 'SuperscriptYOffset' ;
STRIKEOUT_SIZE          : 'StrikeoutSize' ;
STRIKEOUT_POSITION      : 'StrikeoutPosition' ;
WEIGHT_CLASS            : 'WeightClass' ;
WIDTH_CLASS             : 'WidthClass' ;
VENDOR                  : 'Vendor' ;
UNICODE_RANGE           : 'UnicodeRange' ;
CODE_PAGE_RANGE         : 'CodePageRange' ;
FAMILY_CLASS            : 'FamilyClass' ;

STAT                    : 'STAT' ;
ELIDED_FALLBACK_NAME    : 'ElidedFallbackName' ;
ELIDED_FALLBACK_NAME_ID : 'ElidedFallbackNameID' ;
DESIGN_AXIS             : 'DesignAxis' ;
AXIS_VALUE              : 'AxisValue';
FLAG                    : 'flag' ;
LOCATION                : 'location';
AXIS_EAVN               : 'ElidableAxisValueName';
AXIS_OSFA               : 'OlderSiblingFontAttribute';

VHEA                    : 'vhea' ;
VERT_TYPO_ASCENDER      : 'VertTypoAscender' ;
VERT_TYPO_DESCENDER     : 'VertTypoDescender' ;
VERT_TYPO_LINE_GAP      : 'VertTypoLineGap' ;

VMTX                    : 'vmtx' ;
VERT_ORIGIN_Y           : 'VertOriginY' ;
VERT_ADVANCE_Y          : 'VertAdvanceY' ;

LCBRACE                 : '{' ;
RCBRACE                 : '}' ;
LBRACKET                : '[' ;
RBRACKET                : ']' ;
LPAREN                  : '(' -> pushMode(VarValue) ;
RPAREN                  : ')' ;
HYPHEN                  : '-' ;
PLUS                    : '+' ;
SEMI                    : ';' ;
EQUALS                  : '=' ;
MARKER                  : '\'' ;
COMMA                   : ',' ;
COLON                   : ':' ;
STRVAL                  : '"' ( '\\"' | ~["] )* '"' ;

fragment GNST           : 'A' .. 'Z' | 'a' .. 'z' | '_' ;
fragment LCHR           : GNST | '0' .. '9' | '.' ;
fragment GCCHR          : LCHR | '-' ;
LNAME                   : '@' GNST LCHR* ;
GCLASS                  : '@' GNST GCCHR* ;

// AXISUNIT removed from default mode - only exists in LocationDefMode and VarValue
CID                     : '\\' ( '0' .. '9' )+ ;
fragment GNCHR          : GCCHR | '+' | '*' | ':' | '~' | '^' | '|' ;
ESCGNAME                : '\\' GNST GNCHR* ;
NAMELABEL               : GNST LCHR* ;
EXTNAME                 : GNST GNCHR* ;
POINTNUM                : '-'? ( '0' .. '9' )+ '.' ( '0' .. '9' )+ ;
NUMEXT                  : '0x' ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )+ ;
NUMOCT                  : '0' ( '0' .. '7' )+ ;
NUM                     : '-'? ( '1' .. '9' ( '0' .. '9' )* | '0' ) ;

mode Include;

I_WHITESPACE            : [ \t\r\n]+ -> skip ;
I_RPAREN                : '(' -> mode(Ifile) ;

mode Ifile;

IFILE                   : ~')'+ ;
I_LPAREN                : ')' -> popMode ;

// ============================================================================
// LOCATIONDEFMODE (for: locationDef wght=400d, opsz=12d @name;)
// ============================================================================
mode LocationDefMode;

// Axis unit tokens - ONLY defined in this mode
LD_AXISUNIT             : ('u' | 'd' | 'n') -> type(AXISUNIT) ;

// Punctuation needed in location definitions
LD_EQUALS               : '=' -> type(EQUALS) ;
LD_COMMA                : ',' -> type(COMMA) ;
LD_HYPHEN               : '-' -> type(HYPHEN) ;
LD_PLUS                 : '+' -> type(PLUS) ;
LD_SEMI                 : ';' -> type(SEMI), popMode ;  // Exit mode on semicolon

// Identifiers
LD_NAMELABEL            : GNST LCHR* -> type(NAMELABEL) ;  // Axis tags (wght, opsz)
LD_LNAME                : '@' GNST LCHR* -> type(LNAME) ;  // Location name (@Regular)

// Numbers
LD_POINTNUM             : '-'? ( '0' .. '9' )+ '.' ( '0' .. '9' )+ -> type(POINTNUM) ;
LD_NUM                  : '-'? ( '1' .. '9' ( '0' .. '9' )* | '0' ) -> type(NUM) ;

// Whitespace
LD_WHITESPACE           : [ \t\r\n]+ -> skip ;

// NOTE: NO EXTNAME in this mode - prevents d:47 ambiguity

// ============================================================================
// VARVALUE MODE (for: (50 wght=400d:47 @Regular:54))
// ============================================================================
mode VarValue;

// Axis unit tokens - ONLY defined in this mode
VV_AXISUNIT             : ('u' | 'd' | 'n') -> type(AXISUNIT) ;

// Punctuation needed in variable values
VV_COLON                : ':' -> type(COLON) ;          // Key addition for values
VV_EQUALS               : '=' -> type(EQUALS) ;
VV_COMMA                : ',' -> type(COMMA) ;
VV_HYPHEN               : '-' -> type(HYPHEN) ;
VV_PLUS                 : '+' -> type(PLUS) ;
VV_LPAREN               : '(' -> type(LPAREN), pushMode(VarValue) ;  // Nested parens
VV_RPAREN               : ')' -> type(RPAREN), popMode ;  // Exit mode on close paren

// Angle brackets for 4-value positioning records
VV_BEGINVALUE           : '<' -> type(BEGINVALUE) ;
VV_ENDVALUE             : '>' -> type(ENDVALUE) ;

// Identifiers
VV_NAMELABEL            : GNST LCHR* -> type(NAMELABEL) ;  // Axis tags
VV_LNAME                : '@' GNST LCHR* -> type(LNAME) ;  // Location names

// Numbers
VV_POINTNUM             : '-'? ( '0' .. '9' )+ '.' ( '0' .. '9' )+ -> type(POINTNUM) ;
VV_NUM                  : '-'? ( '1' .. '9' ( '0' .. '9' )* | '0' ) -> type(NUM) ;

// Whitespace
VV_WHITESPACE           : [ \t\r\n]+ -> skip ;

// NOTE: NO EXTNAME in this mode - prevents d:47 ambiguity
