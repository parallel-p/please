program Project1;                     // Заголовок программы, с её именем «Project1»
 
uses
  Forms,
  Unit1 in 'Unit1.pas' {Form1};       // модули, которые подключены к проекту и используются программой
 
{$R *.res}
 
begin
  Application.Initialize;                // Инициализация приложения
  Application.CreateForm(TForm1, Form1); // Создание формы/окна
  Application.Run;                       // Запуск и исполнение 
end.
