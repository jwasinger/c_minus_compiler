import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.LinkedList;

public class Tokenizer {
  private LinkedList<Token> tokenRules;
  private LinkedList<Token> codeTokens;
  private String sourceCode;
  private final static Pattern space_regex = Pattern.compile("^(\\s)");
  private final static Pattern tab_regex = Pattern.compile("^(\\t)");

  public Tokenizer(String src) {
    this.tokenRules = new LinkedList<Token>(); 
    this.codeTokens = new LinkedList<Token>();

    this.sourceCode = src;
    
    this.tokenRules.add(new Token(TokenType.TYPE_INT, null, "int"));
    this.tokenRules.add(new Token(TokenType.TYPE_VOID, null, "void"));
    this.tokenRules.add(new Token(TokenType.INT, null, "[0-9]+"));
    this.tokenRules.add(new Token(TokenType.ID, null, "[a-zA-Z][a-zA-Z0-9_]*"));
    this.tokenRules.add(new Token(TokenType.BRACKET_LEFT, null, "\\]"));
    this.tokenRules.add(new Token(TokenType.BRACKET_RIGHT, null, "\\["));
    this.tokenRules.add(new Token(TokenType.BRACE_LEFT, null, "\\}"));
    this.tokenRules.add(new Token(TokenType.BRACE_RIGHT, null, "\\{"));
    this.tokenRules.add(new Token(TokenType.SEMI_COLON, null, "\\;"));
    this.tokenRules.add(new Token(TokenType.IF, null, "if"));
    this.tokenRules.add(new Token(TokenType.ELSE, null, "else"));
    this.tokenRules.add(new Token(TokenType.RETURN, null, "return"));
    this.tokenRules.add(new Token(TokenType.LT_EQ, null, "<="));
    this.tokenRules.add(new Token(TokenType.LT, null, "<"));
    this.tokenRules.add(new Token(TokenType.GT, null, ">"));
    this.tokenRules.add(new Token(TokenType.GT_EQ, null, ">="));
    this.tokenRules.add(new Token(TokenType.EQ_EQ, null, "=="));
    this.tokenRules.add(new Token(TokenType.N_EQ, null, "!="));
    this.tokenRules.add(new Token(TokenType.WHILE, null, "while"));
    this.tokenRules.add(new Token(TokenType.EQ, null, "="));
  }

  public boolean CanConsume() {
    return this.sourceCode.length() != 0;
  }

  private Token consumeNextMatch() throws Exception {
    for (Token token : this.tokenRules) {
      Matcher matcher;
      if ((matcher = token.Match(this.sourceCode)) != null) {
        this.sourceCode = matcher.replaceFirst("");
        return new Token(token.GetType(), "", token.GetRegex());
      }
    }
    
    Matcher space_matcher = space_regex.matcher(this.sourceCode);
    Matcher tab_matcher = tab_regex.matcher(this.sourceCode);

    if (space_matcher.find()) {
      this.sourceCode = space_matcher.replaceFirst("");
      return null;
    } else if (tab_matcher.find()) {
      this.sourceCode = tab_matcher.replaceFirst("");
      return null;
    }
    
    throw new Exception(" token not matched ");
  }

  public static void main(String[]  args) {
    //Pattern space_regex = Pattern.compile("^(\\s)");
    //Pattern tab_regex = Pattern.compile("^(\\t)");

    String regex_str = "\\(";
    Pattern regex = Pattern.compile("^("+regex_str+")");
    String str = "int x = y"; 
    
    Tokenizer tokenizer = new Tokenizer(str);

    try {
      while (tokenizer.CanConsume()) {
        tokenizer.consumeNextMatch();
      }
    } catch (Exception e) {
      System.out.println(e);
    }

    System.out.println("great success!");
  }
}
