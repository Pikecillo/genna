
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.Insets;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.EtchedBorder;
import javax.swing.border.TitledBorder;

public class PlayerWidget extends JPanel {
    private JLabel score;
    private JLabel lines;
    private JLabel level;
    private Engine engine;
    private PlaygroundWidget myPgWidget;
    private NextWidget myNextWidget;

    public NextWidget getNextWidget() {
        return myNextWidget;
    }

    public Engine getEngine() {
        return engine;
    }

    public Insets getInsets() {
        return new Insets(5, 5, 5, 5);
    }

    public void actualizeNumbers(int li, int sc, int le) {
        lines.setText(String.valueOf(li));
        score.setText(String.valueOf(sc));
        level.setText(String.valueOf(le));
    }

    public PlaygroundWidget getPlaygroundWidget() {
        return myPgWidget;
    }

    public PlayerWidget() {
        JPanel panel = new JPanel(), subpanel;

        myPgWidget = new PlaygroundWidget();
        myNextWidget = new NextWidget();
        engine = new Engine(this);
        lines = new JLabel("0");
        score = new JLabel("0");
        level = new JLabel("1");

        setLayout(new BorderLayout());
        panel.setLayout(new GridLayout(4, 1));

        subpanel = new JPanel();
        subpanel.add(myNextWidget);
        subpanel.setBorder(new EtchedBorder());
        panel.add(subpanel);
        subpanel = new JPanel();
        subpanel.add(lines);
        subpanel.setBorder(new TitledBorder("Removed Lines"));
        panel.add(subpanel);
        subpanel = new JPanel();
        subpanel.add(score);
        subpanel.setBorder(new TitledBorder("Score"));
        panel.add(subpanel);
        subpanel = new JPanel();
        subpanel.add(level);
        subpanel.setBorder(new TitledBorder("Level"));
        panel.add(subpanel);
        subpanel = new JPanel();
        subpanel.add(myPgWidget);
        subpanel.setBorder(new EtchedBorder());
        add(subpanel, BorderLayout.WEST);
        add(panel, BorderLayout.EAST);
        setPreferredSize(new Dimension(320, 450));
    }
}
