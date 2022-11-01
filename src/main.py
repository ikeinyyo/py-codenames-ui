from models import CodenameModel
from views import MainView
from viewmodels import MainViewmodel


def main():
    model = CodenameModel('es', 5, 5)
    viewmodel = MainViewmodel(model)
    view = MainView(viewmodel)

    view.run()


if __name__ == "__main__":
    main()
