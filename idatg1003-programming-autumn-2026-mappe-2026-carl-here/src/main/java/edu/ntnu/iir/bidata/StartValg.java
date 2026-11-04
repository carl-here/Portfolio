package edu.ntnu.iir.bidata;

/**
 * Klassen enum er startvalgene.
 */
public enum StartValg {
  REGISTRER, SLETT;

  /**
   * Tar inn valg fra bruker.
   */
  public static StartValg fromMenuOption(int valg) {
    return switch (valg) {
      case 1 -> REGISTRER;
      case 2 -> SLETT;
      default -> throw new IllegalArgumentException(
          "Beklager, jeg kjenner ikke til den kommandoen: " + valg);
    };
  }
}
