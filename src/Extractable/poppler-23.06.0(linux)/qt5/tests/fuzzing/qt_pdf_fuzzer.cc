#include <cstdint>
#include <poppler-qt5.h>
#include <QtCore/QBuffer>
#include <QtGui/QImage>

static void dummy_error_function(const QString &, const QVariant &) { }

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    Poppler::setDebugErrorFunction(dummy_error_function, QVariant());
    QByteArray in_data = QByteArray::fromRawData((const char *)data, size);
    Poppler::Document *doc = Poppler::Document::loadFromData(in_data);
    if (!doc || doc->isLocked()) {
        delete doc;
        return 0;
    }

    for (int i = 0; i < doc->numPages(); i++) {
        Poppler::Page *p = doc->page(i);
        if (!p) {
            continue;
        }
        QImage image = p->renderToImage(72.0, 72.0, -1, -1, -1, -1, Poppler::Page::Rotate0);
        delete p;
    }

    if (doc->numPages() > 0) {
        QList<int> pageList;
        for (int i = 0; i < doc->numPages(); i++) {
            pageList << (i + 1);
        }

        Poppler::PSConverter *psConverter = doc->psConverter();

        QBuffer buffer;
        buffer.open(QIODevice::WriteOnly);
        psConverter->setOutputDevice(&buffer);

        psConverter->setPageList(pageList);
        psConverter->setPaperWidth(595);
        psConverter->setPaperHeight(842);
        psConverter->setTitle(doc->info("Title"));
        psConverter->convert();
        delete psConverter;
    }

    delete doc;
    return 0;
}
