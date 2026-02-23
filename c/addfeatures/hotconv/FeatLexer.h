
// Generated from FeatLexer.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  FeatLexer : public antlr4::Lexer {
public:
  enum {
    AXISUNIT = 1, ANON = 2, ANON_v = 3, COMMENT = 4, WHITESPACE = 5, INCLUDE = 6, 
    FEATURE = 7, TABLE = 8, SCRIPT = 9, LANGUAGE = 10, LANGSYS = 11, SUBTABLE = 12, 
    LOOKUP = 13, LOOKUPFLAG = 14, NOTDEF = 15, RIGHT_TO_LEFT = 16, IGNORE_BASE_GLYPHS = 17, 
    IGNORE_LIGATURES = 18, IGNORE_MARKS = 19, USE_MARK_FILTERING_SET = 20, 
    MARK_ATTACHMENT_TYPE = 21, EXCLUDE_DFLT = 22, INCLUDE_DFLT = 23, EXCLUDE_dflt = 24, 
    INCLUDE_dflt = 25, USE_EXTENSION = 26, BEGINVALUE = 27, ENDVALUE = 28, 
    ENUMERATE = 29, ENUMERATE_v = 30, EXCEPT = 31, IGNORE = 32, SUBSTITUTE = 33, 
    SUBSTITUTE_v = 34, REVERSE = 35, REVERSE_v = 36, BY = 37, FROM = 38, 
    POSITION = 39, POSITION_v = 40, PARAMETERS = 41, FEATURE_NAMES = 42, 
    CV_PARAMETERS = 43, CV_UI_LABEL = 44, CV_TOOLTIP = 45, CV_SAMPLE_TEXT = 46, 
    CV_PARAM_LABEL = 47, CV_CHARACTER = 48, SIZEMENUNAME = 49, CONTOURPOINT = 50, 
    ANCHOR = 51, ANCHOR_DEF = 52, VALUE_RECORD_DEF = 53, LOCATION_DEF = 54, 
    MARK = 55, MARK_CLASS = 56, CURSIVE = 57, MARKBASE = 58, MARKLIG = 59, 
    MARKLIG_v = 60, LIG_COMPONENT = 61, KNULL = 62, BASE = 63, HA_BTL = 64, 
    VA_BTL = 65, HA_BSL = 66, VA_BSL = 67, GDEF = 68, GLYPH_CLASS_DEF = 69, 
    ATTACH = 70, LIG_CARET_BY_POS = 71, LIG_CARET_BY_IDX = 72, HEAD = 73, 
    FONT_REVISION = 74, HHEA = 75, ASCENDER = 76, DESCENDER = 77, LINE_GAP = 78, 
    CARET_OFFSET = 79, CARET_SLOPE_RISE = 80, CARET_SLOPE_RUN = 81, NAME = 82, 
    NAMEID = 83, OS_2 = 84, FS_TYPE = 85, FS_TYPE_v = 86, OS2_LOWER_OP_SIZE = 87, 
    OS2_UPPER_OP_SIZE = 88, PANOSE = 89, TYPO_ASCENDER = 90, TYPO_DESCENDER = 91, 
    TYPO_LINE_GAP = 92, WIN_ASCENT = 93, WIN_DESCENT = 94, X_HEIGHT = 95, 
    CAP_HEIGHT = 96, SUBSCRIPT_X_SIZE = 97, SUBSCRIPT_X_OFFSET = 98, SUBSCRIPT_Y_SIZE = 99, 
    SUBSCRIPT_Y_OFFSET = 100, SUPERSCRIPT_X_SIZE = 101, SUPERSCRIPT_X_OFFSET = 102, 
    SUPERSCRIPT_Y_SIZE = 103, SUPERSCRIPT_Y_OFFSET = 104, STRIKEOUT_SIZE = 105, 
    STRIKEOUT_POSITION = 106, WEIGHT_CLASS = 107, WIDTH_CLASS = 108, VENDOR = 109, 
    UNICODE_RANGE = 110, CODE_PAGE_RANGE = 111, FAMILY_CLASS = 112, STAT = 113, 
    ELIDED_FALLBACK_NAME = 114, ELIDED_FALLBACK_NAME_ID = 115, DESIGN_AXIS = 116, 
    AXIS_VALUE = 117, FLAG = 118, LOCATION = 119, AXIS_EAVN = 120, AXIS_OSFA = 121, 
    VHEA = 122, VERT_TYPO_ASCENDER = 123, VERT_TYPO_DESCENDER = 124, VERT_TYPO_LINE_GAP = 125, 
    VMTX = 126, VERT_ORIGIN_Y = 127, VERT_ADVANCE_Y = 128, LCBRACE = 129, 
    RCBRACE = 130, LBRACKET = 131, RBRACKET = 132, LPAREN = 133, RPAREN = 134, 
    HYPHEN = 135, PLUS = 136, SEMI = 137, EQUALS = 138, MARKER = 139, COMMA = 140, 
    COLON = 141, STRVAL = 142, LNAME = 143, GCLASS = 144, CID = 145, ESCGNAME = 146, 
    NAMELABEL = 147, EXTNAME = 148, POINTNUM = 149, NUMEXT = 150, NUMOCT = 151, 
    NUM = 152, A_WHITESPACE = 153, A_LABEL = 154, A_LBRACE = 155, A_CLOSE = 156, 
    A_LINE = 157, I_WHITESPACE = 158, I_RPAREN = 159, IFILE = 160, I_LPAREN = 161, 
    LD_WHITESPACE = 162, VV_WHITESPACE = 163
  };

  enum {
    Anon = 1, AnonContent = 2, Include = 3, Ifile = 4, LocationDefMode = 5, 
    VarValue = 6
  };

  explicit FeatLexer(antlr4::CharStream *input);

  ~FeatLexer() override;


   std::string anon_tag;

   /* All the TSTART/TCHR characters are grouped together, so just
    * look for the string and if its there verify that the characters
    * on either side are from the appropriate set (in case there are
    * "extra" characters).
    */

   bool verify_anon(const std::string &line) {
       auto p = line.find(anon_tag);
       if ( p == std::string::npos )
           return false;
       --p;
       if ( ! ( line[p] == ' ' || line[p] == '\t' || line[p] == '}' ) )
           return false;
       p += anon_tag.size() + 1;
       if ( ! ( line[p] == ' ' || line[p] == '\t' || line[p] == ';' ) )
           return false;
       return true;
   }


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  void action(antlr4::RuleContext *context, size_t ruleIndex, size_t actionIndex) override;

  bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.
  void A_LABELAction(antlr4::RuleContext *context, size_t actionIndex);

  // Individual semantic predicate functions triggered by sempred() above.
  bool A_CLOSESempred(antlr4::RuleContext *_localctx, size_t predicateIndex);

};

