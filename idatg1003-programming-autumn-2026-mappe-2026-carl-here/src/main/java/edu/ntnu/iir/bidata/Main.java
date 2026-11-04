package edu.ntnu.iir.bidata;

/**
 * Klassen Main kjører programmet.
 */
public class Main {
  public static void main(String[] args) {
    while (true) {
      BrukerGrensesnittet meny = new BrukerGrensesnittet();
      meny.start();
    }
  }
}
