/*
#include <QApplication>
#include <QLabel>
#include <QPushButton>
#include <QRandomGenerator> 
#include <QVBoxLayout>
#include <QWidget>


size_t my_random() {
  return QRandomGenerator::global()->generate();
}


class MyWidget : public QWidget {
public:
  MyWidget() :
    hello({"Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"}),
    button("Click me!"),
    text("Hello World"),
    layout(this)
  {
    text.setAlignment(Qt::AlignCenter);

    layout.addWidget(&text);
    layout.addWidget(&button);

    connect(&button, &QPushButton::clicked, this, &MyWidget::magic);
  }
  
  void magic() {
    text.setText(hello[my_random() % hello.size()]);
  }
  
private:
  std::vector<QString> hello;
  QPushButton button;
  QLabel text;
  QVBoxLayout layout;
  
};

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  
  
  MyWidget widget;
  widget.resize(800, 600);
  widget.show();

  return app.exec();
}
*/